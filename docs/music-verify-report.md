# 音乐内容级验证报告

> 生成：2026-09-17T21:21:42 · 全库 94,740 首

## 一、正常基线（P1 / 中位 / P99）

| 指标 | P1 | 中位 | P99 |
|---|---:|---:|---:|
| notes | 20 | 262 | 8982 |
| dur | 5.8 | 63.5 | 964.7 |
| density | 1.2 | 4.1 | 17.6 |
| tonality | 0.0 | 0.826 | 0.972 |
| motif | 0.0 | 0.485 | 1.0 |

## 二、验证结果

- ✅ 正常：**92,476**
- 🔴 hard-fail（内容损坏级）：**569**
- 🟡 suspect（可疑）：**1,695**

hard-fail 按源：groove 278, chinafolk 119, musedata 88, oga 34, essen 33, musicnet 7, thesession 5, m21 4, norbeck 1

### hard-fail 明细（前 40）

- chinafolk-000006·chinafolk·运河大船摇橹号子 → 音符过少(12)
- chinafolk-000403·chinafolk·卖西瓜（三） → 音符过少(13)
- chinafolk-000420·chinafolk·卖江米藕 → 音符过少(9)
- chinafolk-000425·chinafolk·卖老玉米（二） → 音符过少(13)
- chinafolk-000426·chinafolk·卖糖葫芦（一） → 音符过少(10)
- chinafolk-000427·chinafolk·卖糖葫芦（二） → 音符过少(13)
- chinafolk-000428·chinafolk·卖大糖葫芦 → 音符过少(10)
- chinafolk-000429·chinafolk·卖大挂山里红 → 音符过少(11)
- chinafolk-000430·chinafolk·卖果子干 → 音符过少(12)
- chinafolk-000431·chinafolk·卖冰核（一） → 音符过少(14)
- chinafolk-000432·chinafolk·卖冰核（二） → 音符过少(8)
- chinafolk-000434·chinafolk·卖冰棍（二） → 音符过少(14)
- chinafolk-000435·chinafolk·卖奶酪 → 音符过少(10)
- chinafolk-000436·chinafolk·卖香仁茶 → 音符过少(10)
- chinafolk-000438·chinafolk·卖熟豆汁 → 音符过少(6); 时长过短(2.6s)
- chinafolk-000441·chinafolk·卖馄饨 → 音符过少(5); 时长过短(2.3s)
- chinafolk-000443·chinafolk·卖扒糕凉粉（一） → 音符过少(13)
- chinafolk-000444·chinafolk·卖扒糕凉粉（二） → 音符过少(13)
- chinafolk-000445·chinafolk·卖凉糕 → 音符过少(14)
- chinafolk-000446·chinafolk·卖蜂糕艾窝窝 → 音符过少(14)
- chinafolk-000454·chinafolk·卖梨膏 → 音符过少(13)
- chinafolk-000462·chinafolk·卖硬面饽饽（二） → 音符过少(10)
- chinafolk-000463·chinafolk·卖硬面饽饽（三） → 音符过少(6)
- chinafolk-000464·chinafolk·卖烤白薯 → 音符过少(14)
- chinafolk-000473·chinafolk·卖豆芽菜 → 音符过少(10)
- chinafolk-000474·chinafolk·卖萝卜（一） → 音符过少(11)
- chinafolk-000487·chinafolk·卖松枝芝麻秸 → 音符过少(8)
- chinafolk-000488·chinafolk·卖画（一） → 音符过少(10); 时长过短(2.8s)
- chinafolk-000489·chinafolk·卖画（二） → 音符过少(6); 时长过短(2.3s)
- chinafolk-000490·chinafolk·卖画挂签 → 音符过少(10)
- chinafolk-000491·chinafolk·卖蒲帘子 → 音符过少(13)
- chinafolk-000497·chinafolk·磨剪子抢菜刀（一） → 音符过少(10)
- chinafolk-000498·chinafolk·磨剪子抢菜刀（二） → 音符过少(9)
- chinafolk-000499·chinafolk·抢剪子磨刀 → 音符过少(10)
- chinafolk-000501·chinafolk·焊洋铁壶 → 音符过少(9)
- chinafolk-000505·chinafolk·夹包打鼓的 → 音符过少(9)
- chinafolk-000506·chinafolk·挑挑打鼓的 → 音符过少(8); 时长过短(2.6s)
- chinafolk-000638·chinafolk·正月桃花月色新 → 音符过少(14)
- chinafolk-000786·chinafolk·卖雪条 → 音符过少(6); 时长过短(1.9s)
- chinafolk-000787·chinafolk·卖粉藕 → 音符过少(11)

### suspect 明细（前 40）

- aria-000424·aria· → 无动机重复(0.011)
- aria-000539·aria· → 无动机重复(0.011)
- aria-000630·aria· → 无动机重复(0.014)
- aria-000782·aria· → 无动机重复(0.011)
- aria-000818·aria· → 无动机重复(0.005)
- aria-000900·aria· → 无动机重复(0.023)
- aria-001320·aria· → 无动机重复(0.026)
- aria-001327·aria· → 音域过宽(90)
- aria-001387·aria· → 无动机重复(0.017)
- aria-001418·aria· → 无动机重复(0.019)
- aria-001426·aria· → 无动机重复(0.025)
- aria-001463·aria· → 无动机重复(0.016)
- aria-001955·aria· → 无动机重复(0.021)
- aria-001958·aria· → 无动机重复(0.026)
- aria-002174·aria· → 无动机重复(0.021)
- aria-002508·aria· → 时长超长(2602.4s)
- aria-002671·aria· → 无动机重复(0.019)
- aria-002682·aria· → 时长超长(4613.9s)
- aria-002765·aria· → 无动机重复(0.022)
- aria-003174·aria· → 无动机重复(0.015)
- aria-003479·aria· → 时长超长(2228.8s)
- aria-003482·aria· → 无动机重复(0.028)
- aria-003512·aria· → 无动机重复(0.019)
- aria-003568·aria· → 时长超长(2144.4s)
- aria-003608·aria· → 无动机重复(0.0)
- aria-003733·aria· → 无动机重复(0.012)
- aria-003773·aria· → 时长超长(3438.4s)
- aria-003776·aria· → 无动机重复(0.025)
- aria-003804·aria· → 无动机重复(0.025)
- aria-003977·aria· → 时长超长(4444.4s)
- aria-004440·aria· → 无动机重复(0.009)
- aria-004508·aria· → 无动机重复(0.02)
- aria-004528·aria· → 无动机重复(0.01)
- aria-004760·aria· → 无动机重复(0.016)
- aria-005445·aria· → 无动机重复(0.0)
- aria-005474·aria· → 无动机重复(0.017)
- aria-005488·aria· → 无动机重复(0.024)
- aria-005564·aria· → 无动机重复(0.016)
- aria-005609·aria· → 无动机重复(0.007)
- aria-005876·aria· → 无动机重复(0.02)

## 三、处置建议

1. hard-fail：从发布集排除（保留记录，加 `verify_flag=hard`）
2. suspect：抽人工核听（数量大则按源分批）
3. 确认无问题的 hard-fail（如极短的练习曲片段）可人工恢复