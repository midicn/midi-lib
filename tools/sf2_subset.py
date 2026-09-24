#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SF2 子集化 —— 只保留实际用到的预置，重写一个等价但更小的 SoundFont。

为什么做
--------
站点用的是 GeneralUser GS（32.3 MB），而全库 **只用到 2 个 bank**：
`bank 0` 的 86 个音色 + `bank 128` 的 12 个鼓组（抽样 3000 首实测）。
GS 变体库（bank 1–26、120）**完全没被用到**。
文件 99% 的体积是采样数据，所以裁掉用不到的预置 = 直接省下对应采样。

用法
----
    python sf2_subset.py --report                    # 只报告：各方案省多少（不改文件）
    python sf2_subset.py --build --keep used         # 生成子集（保留实测用到的）
    python sf2_subset.py --build --keep gm-all       # 生成子集（保留全部 bank0 + 鼓组，最保守）
    python sf2_subset.py --verify <子集.sf2>         # 校验：结构 + 采样字节逐一比对

设计要点
--------
· **不改采样内容**：只搬运字节，逐采样校验与原文件一致（可验证的零损失）。
· `smpl` 块里每个采样前有 46 字节头；SHDR 的 start/end 指向**头之后的采样数据**，
  故搬运区间取 `[start-46, end)`，新 start = 新块偏移 + 46。
· IGEN 的 `sampleID`（oper 43）与 PGEN 的 `instrument`（oper 41）**必须重映射**。
· 保留 SHDR 末尾的 EOS 记录，并把它的 start/end 指到新 smpl 末尾。
"""
from __future__ import annotations

import argparse
import os
import struct
import sys
from pathlib import Path

# SF2 generator 操作符
GEN_INSTRUMENT = 41     # PGEN: 指向 instrument
GEN_SAMPLE_ID = 53      # IGEN: 指向 sample（注意：53 才是 sampleID；43=keyRange、44=velRange）

EOP = 0                 # 结束标记


# ─────────────────────────────────────────────────────────────── 解析

def riff_chunks(buf: bytes, start: int, end: int):
    """遍历 start..end 的 RIFF 块，yield (id, size, data_offset)。"""
    pos = start
    while pos + 8 <= end:
        cid = buf[pos:pos + 4]
        sz = struct.unpack("<I", buf[pos + 4:pos + 8])[0]
        yield cid, sz, pos + 8
        pos += 8 + sz + (sz & 1)


class Sf2:
    def __init__(self, buf: bytes):
        self.buf = buf
        self.tables: dict[str, tuple[int, int]] = {}
        self.info: dict[str, bytes] = {}
        self.smpl = (0, 0)
        self._parse()

    def _parse(self):
        b = self.buf
        sdta = pdta = None
        for cid, sz, data in riff_chunks(b, 12, len(b)):
            if cid != b"LIST":
                continue
            kind = b[data:data + 4]
            if kind == b"INFO":
                for c, s, d in riff_chunks(b, data + 4, data + sz):
                    self.info[c.decode("latin1")] = b[d:d + s]
            elif kind == b"sdta":
                sdta = (data + 4, data + sz)
            elif kind == b"pdta":
                pdta = (data + 4, data + sz)
        for cid, sz, data in riff_chunks(b, *sdta):
            if cid == b"smpl":
                self.smpl = (data, sz)
        for cid, sz, data in riff_chunks(b, *pdta):
            self.tables[cid.decode("latin1")] = (data, sz)

    # ---- 各表记录读取 ----
    def u16(self, off):
        return struct.unpack("<H", self.buf[off:off + 2])[0]

    def u32(self, off):
        return struct.unpack("<I", self.buf[off:off + 4])[0]

    def name20(self, off):
        return self.buf[off:off + 20].rstrip(b"\x00").decode("latin1", "replace")

    def presets(self):
        """[(bank, preset, name, bag_index)]（含末尾 EOS 记录）"""
        base, sz = self.tables["phdr"]
        out = []
        for i in range(sz // 38):
            o = base + i * 38
            pre, bank, bag = struct.unpack("<HHH", self.buf[o + 20:o + 26])
            out.append((bank, pre, self.name20(o), bag))
        return out

    def instruments(self):
        """[(name, bag_index)]（含末尾 EOI 记录）"""
        base, sz = self.tables["inst"]
        out = []
        for i in range(sz // 22):
            o = base + i * 22
            out.append((self.name20(o), self.u16(o + 20)))
        return out

    def samples(self):
        """SHDR 记录（含末尾 EOS）"""
        base, sz = self.tables["shdr"]
        out = []
        for i in range(sz // 46):
            o = base + i * 46
            start, end, sloop, eloop = struct.unpack("<IIII", self.buf[o + 20:o + 36])
            rate, pitch, corr, link, stype = struct.unpack("<IBbHH", self.buf[o + 36:o + 46])
            out.append(dict(idx=i, name=self.name20(o), start=start, end=end,
                            startloop=sloop, endloop=eloop, rate=rate, pitch=pitch,
                            corr=corr, link=link, stype=stype, raw=o))
        return out

    def zones(self, bag_name: str, gen_name: str, start_bag: int, end_bag: int):
        """返回 start_bag..end_bag 每个 zone 的 generator 列表 [(oper, amount)]。

        每条 bag 记录 = (genNdx, modNdx)；generator 段延伸到**下一条 bag 的 genNdx**。
        """
        bag_base, _ = self.tables[bag_name]
        gen_base, _ = self.tables[gen_name]
        out = []
        for k in range(start_bag, end_bag):
            gs = self.u16(bag_base + k * 4)
            ge = self.u16(bag_base + (k + 1) * 4) if k + 1 < end_bag else gs
            gens = []
            for g in range(gs, ge):
                oper = self.u16(gen_base + g * 4)
                amt = self.u16(gen_base + g * 4 + 2)
                if oper == EOP:
                    break
                gens.append((oper, amt))
            out.append(gens)
        return out

    # ---- 关系图 ----
    def preset_to_inst(self) -> dict[tuple[int, int], list[int]]:
        pre = self.presets()
        out = {}
        for i in range(len(pre) - 1):
            bank, pr, _, bag = pre[i]
            end = pre[i + 1][3]
            ids = []
            for gens in self.zones("pbag", "pgen", bag, end):
                for oper, amt in gens:
                    if oper == GEN_INSTRUMENT:
                        ids.append(amt)
            out[(bank, pr)] = ids
        return out

    def inst_to_smp(self) -> dict[int, list[int]]:
        ins = self.instruments()
        n_smp = self.tables["shdr"][1] // 46
        out = {}
        for i in range(len(ins) - 1):
            _, bag = ins[i]
            end = ins[i + 1][1]
            ids = []
            for gens in self.zones("ibag", "igen", bag, end):
                for oper, amt in gens:
                    if oper == GEN_SAMPLE_ID and amt < n_smp:
                        ids.append(amt)
            out[i] = ids
        return out

    def sample_bytes(self, idx: int) -> int:
        sh = self.samples()[idx]
        return max(0, sh["end"] - sh["start"])


# ─────────────────────────────────────────────────────────────── 方案

# 抽样 3000 首实测：全库只用到这两个 bank
USED_BANK0 = {0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 19, 20, 21, 22, 23, 24,
              25, 26, 27, 28, 29, 32, 33, 34, 35, 36, 40, 41, 42, 43, 44, 45, 46, 47, 48,
              49, 50, 51, 52, 53, 54, 56, 57, 58, 59, 60, 61, 62, 64, 65, 66, 67, 68, 69,
              70, 71, 72, 73, 74, 75, 76, 80, 82, 88, 89, 91, 93, 94, 95, 100, 101, 102,
              105, 106, 107, 110, 111, 115, 119, 126, 127}
USED_DRUMS = {0, 25, 40, 48, 49, 56, 58, 59, 83, 96, 115, 127}


def keep_indices(sf: Sf2, mode: str) -> set[int]:
    """返回要保留的**预置索引**集合。

    ⚠️ 用索引而非 (bank, preset)：GeneralUser GS 里 bank 0 有 129 条预置
    （GM 标准只有 128），存在同号预置；按 pair 去重会**丢掉 76 条**。
    """
    pre = sf.presets()
    idx = set()
    for i in range(len(pre) - 1):
        bank, pr = pre[i][0], pre[i][1]
        if mode == "all":
            idx.add(i)
        elif mode == "used":
            if (bank == 0 and pr in USED_BANK0) or (bank == 128 and pr in USED_DRUMS):
                idx.add(i)
        elif mode == "gm-all":
            if bank == 0 or bank in (120, 128):
                idx.add(i)
        elif mode == "bank0":
            if bank == 0:
                idx.add(i)
        else:
            raise SystemExit(f"未知 --keep 模式：{mode}")
    return idx


def measure(sf: Sf2, keep_idx: set[int]):
    p2i = sf.preset_to_inst()
    i2s = sf.inst_to_smp()
    pre = sf.presets()
    smps, insts = set(), set()
    for i in keep_idx:
        for ii in p2i.get((pre[i][0], pre[i][1]), []):
            insts.add(ii)
            smps.update(i2s.get(ii, []))
    nbytes = sum(sf.sample_bytes(i) for i in smps)
    return len(smps), len(insts), nbytes


# ─────────────────────────────────────────────────────────────── 重写

def put_chunk(buf: bytearray, cid: bytes, data: bytes):
    buf += cid + struct.pack("<I", len(data)) + data
    if len(data) & 1:
        buf += b"\x00"


def build(sf: Sf2, keep_idx: set[int]) -> bytes:
    b = sf.buf
    p2i = sf.preset_to_inst()
    i2s = sf.inst_to_smp()
    pre = sf.presets()
    ins = sf.instruments()

    # ① 展开保留集：预置 → 乐器 → 采样
    insts, smps = set(), set()
    for i in sorted(keep_idx):
        for ii in p2i.get((pre[i][0], pre[i][1]), []):
            insts.add(ii)
            smps.update(i2s.get(ii, []))
    insts = sorted(insts)
    smps = sorted(i for i in smps if i < len(sf.samples()) - 1)
    inst_map = {old: new for new, old in enumerate(insts)}
    smp_map = {old: new for new, old in enumerate(smps)}

    # ② 重建 smpl：逐采样搬 [start-46, end)
    old_smpl_off, _ = sf.smpl
    shdrs = sf.samples()
    new_smpl = bytearray()
    meta = []
    for old in smps:
        sh = shdrs[old]
        block = len(new_smpl)            # 本采样 46 字节头的新位置
        new_smpl += b[old_smpl_off + sh["start"] - 46: old_smpl_off + sh["end"]]
        if len(new_smpl) & 1:
            new_smpl += b"\x00"
        # 新 start = 块首 + 46；delta 相对老 start 计算（**不能用 len(new_smpl) 推**，
        # 否则遇到奇数字节填充会整体偏移 1）
        delta = (block + 46) - sh["start"]
        meta.append(dict(name=sh["name"], start=sh["start"] + delta, end=sh["end"] + delta,
                         startloop=sh["startloop"] + delta, endloop=sh["endloop"] + delta,
                         rate=sh["rate"], pitch=sh["pitch"], corr=sh["corr"],
                         link=sh["link"], stype=sh["stype"]))
    eos = len(new_smpl) + 46
    meta.append(dict(name="EOS", start=eos, end=eos, startloop=eos, endloop=eos,
                     rate=0, pitch=255, corr=0, link=0, stype=0))

    # ③ igen / ibag / inst（按新采样索引重映射）
    ibag, igen = bytearray(), bytearray()
    inst_recs, acc = [], 0
    for old_i in insts:
        _, bag = ins[old_i]
        end = ins[old_i + 1][1]
        inst_recs.append((ins[old_i][0], acc))
        n_zone = 0
        for gens in sf.zones("ibag", "igen", bag, end):
            ibag += struct.pack("<HH", len(igen) // 4, 0)
            for oper, amt in gens:
                if oper == GEN_SAMPLE_ID:
                    if amt not in smp_map:
                        continue
                    amt = smp_map[amt]
                igen += struct.pack("<HH", oper, amt)
            igen += struct.pack("<HH", EOP, 0)
            n_zone += 1
        acc += n_zone
    ibag += struct.pack("<HH", len(igen) // 4, 0)
    inst_recs.append(("EOI", acc))
    inst_blob = bytearray()
    for nm, bi in inst_recs:
        inst_blob += nm.encode("latin1")[:19].ljust(20, b"\x00") + struct.pack("<H", bi)

    # ④ pgen / pbag / phdr（按乐器索引重映射；**保序**，含同号预置）
    pbag, pgen = bytearray(), bytearray()
    phdr = bytearray()
    acc = 0
    for i in sorted(keep_idx):
        phdr += pre[i][2].encode("latin1")[:19].ljust(20, b"\x00")
        # PHDR 记录固定 38 字节：name(20) + preset(2) + bank(2) + bagNdx(2)
        #                          + library(4) + genre(4) + morphology(4)
        phdr += struct.pack("<HHH", pre[i][1], pre[i][0], acc)
        phdr += struct.pack("<III", 0, 0, 0)
        bag, end = pre[i][3], pre[i + 1][3]
        n_zone = 0
        for gens in sf.zones("pbag", "pgen", bag, end):
            pbag += struct.pack("<HH", len(pgen) // 4, 0)
            for oper, amt in gens:
                if oper == GEN_INSTRUMENT:
                    if amt not in inst_map:
                        continue
                    amt = inst_map[amt]
                pgen += struct.pack("<HH", oper, amt)
            pgen += struct.pack("<HH", EOP, 0)
            n_zone += 1
        acc += n_zone
    pbag += struct.pack("<HH", len(pgen) // 4, 0)
    phdr += b"EOP".ljust(20, b"\x00") + struct.pack("<HHH", 0, 0, acc) + struct.pack("<III", 0, 0, 0)

    # ⑤ shdr
    shdr = bytearray()
    for m in meta:
        shdr += m["name"].encode("latin1")[:19].ljust(20, b"\x00")
        shdr += struct.pack("<IIII", m["start"], m["end"], m["startloop"], m["endloop"])
        shdr += struct.pack("<IBbHH", m["rate"], m["pitch"], m["corr"], m["link"], m["stype"])

    # ⑥ 组装
    info = bytearray()
    for k, v in sf.info.items():
        if k == "ICMT":
            v = v[:256]
    # 补齐所有 INFO 块
    for k, v in sf.info.items():
        put_chunk(info, k.encode("latin1"), v[:256] if k == "ICMT" else v)
    pdta = bytearray()
    for cid, blob in (("phdr", phdr), ("pbag", pbag), ("pmod", b"\x00" * 10), ("pgen", pgen),
                      ("inst", inst_blob), ("ibag", ibag), ("imod", b"\x00" * 10),
                      ("igen", igen), ("shdr", shdr)):
        put_chunk(pdta, cid.encode("latin1"), bytes(blob))
    smpl_body = bytearray()
    put_chunk(smpl_body, b"smpl", bytes(new_smpl))

    out = bytearray(b"RIFF\x00\x00\x00\x00sfbk")
    for tag, payload in ((b"INFO", info), (b"sdta", smpl_body), (b"pdta", pdta)):
        lh = bytearray(b"LIST" + b"\x00\x00\x00\x00" + tag)
        lh[4:8] = struct.pack("<I", len(payload) + 4)
        out += lh + payload
    out[4:8] = struct.pack("<I", len(out) - 8)
    import sys as _s
    if os.environ.get("SF2_DEBUG"):
        print("  [dbg] phdr 记录 %d（含 EOP）· inst %d（含 EOI）· shdr %d（含 EOS）"
              % (len(phdr) // 38, len(inst_blob) // 22, len(shdr) // 46), file=_s.stderr)
        print("  [dbg] pbag %d · pgen %d · ibag %d · igen %d"
              % (len(pbag) // 4, len(pgen) // 4, len(ibag) // 4, len(igen) // 4), file=_s.stderr)
    return bytes(out)


def verify(orig: Sf2, sub_path: Path) -> bool:
    sub = Sf2(sub_path.read_bytes())
    ok = True
    print("  原始：预置 %d · 乐器 %d · 采样 %d" %
          (len(orig.presets()) - 1, len(orig.instruments()) - 1, len(orig.samples()) - 1))
    print("  子集：预置 %d · 乐器 %d · 采样 %d" %
          (len(sub.presets()) - 1, len(sub.instruments()) - 1, len(sub.samples()) - 1))
    # 结构自检：采样偏移必须在 smpl 范围内且递增
    smpl_sz = sub.smpl[1]
    prev_end = 0
    bad = 0
    for sh in sub.samples()[:-1]:
        if not (46 <= sh["start"] <= sh["end"] <= smpl_sz) or sh["start"] < prev_end:
            bad += 1
        prev_end = sh["end"]
    print("  %s 采样偏移自检：%d 处异常" % ("✓" if bad == 0 else "✗", bad))
    ok &= bad == 0
    # 采样字节逐一比对（同名采样在新旧文件中内容必须一致）
    o_smp = {s["name"]: s for s in orig.samples()[:-1]}
    mism = []
    for s in sub.samples()[:-1]:
        o = o_smp.get(s["name"])
        if not o:
            mism.append(s["name"] + "(缺失于原文件)"); continue
        a = orig.buf[orig.smpl[0] + o["start"]: orig.smpl[0] + o["end"]]
        c = sub.buf[sub.smpl[0] + s["start"]: sub.smpl[0] + s["end"]]
        if a != c:
            mism.append(s["name"])
    print("  %s 采样内容比对：%d 处不一致" % ("✓" if not mism else "✗", len(mism)))
    if mism:
        print("     ", mism[:8])
    ok &= not mism
    return ok


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(Path(__file__).resolve().parents[2] /
                                         "site" / "soundfont" / "GeneralUser-GS.sf2"))
    ap.add_argument("--out", default="")
    ap.add_argument("--keep", default="all", choices=["all", "used", "gm-all", "bank0"])
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", default="")
    a = ap.parse_args(argv[1:])

    if a.verify:
        o = Sf2(Path(a.src).read_bytes())
        return 0 if verify(o, Path(a.verify)) else 1

    src = Path(a.src)
    sf = Sf2(src.read_bytes())
    total = sum(sf.sample_bytes(i) for i in range(len(sf.samples()) - 1))
    print("源文件 %s" % src.name)
    print("  预置 %d · 乐器 %d · 采样 %d · 采样数据 %.1f MB · 文件 %.1f MB" %
          (len(sf.presets()) - 1, len(sf.instruments()) - 1, len(sf.samples()) - 1,
           total / 1e6, src.stat().st_size / 1e6))
    print()
    for mode in ("bank0", "used", "gm-all", "all"):
        kp = keep_indices(sf, mode)
        ns, ni, nb = measure(sf, kp)
        print("  --keep %-7s 预置 %3d · 乐器 %3d · 采样 %3d · 采样数据 %6.1f MB (%.0f%%)"
              % (mode, len(kp), ni, ns, nb / 1e6, nb / total * 100))

    if a.build:
        kp = keep_indices(sf, a.keep)
        out = Path(a.out) if a.out else src.with_name("GeneralUser-GS-subset.sf2")
        data = build(sf, kp)
        out.write_bytes(data)
        print("\n已生成 %s  %.1f MB  （原 %.1f MB，省 %.0f%%）" %
              (out, len(data) / 1e6, src.stat().st_size / 1e6,
               (1 - len(data) / src.stat().st_size) * 100))
        print("校验：")
        return 0 if verify(sf, out) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
