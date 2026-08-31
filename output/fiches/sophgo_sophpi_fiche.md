---
## sophgo/sophpi [MODIFIÉ]
**Type:** Library
**Domain:** Embedded
**Relevance score:** 78/100
**Problem solved:** CV18xx系列 SOC 开源硬件平台
**How it works:** # 快速入门指南

## V410 SDK 编译步骤

### 获取源码

步骤一:

``` bash
mkdir -p <WORKSPACE>
cd <WORKSPACE>
git clone -b sg200x-evb git@github.com:sophgo/sophpi.git
./sophpi/scripts/repo_clone.sh --gitclone sophpi/scripts/subtree.xml
```

步骤二:

``` bash
source build/envsetup_soc.sh
defconfig sg2002_wevb_riscv64_sd
cle
**Chinese specificity:** Chinese open-source project
**Western equivalent:** Not identified
**Maturity:** Active (★ 60, 35 forks, updated 2026-08)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/sophgo/sophpi
---
