---
## sophgo/sophpi [MODIFIÉ]
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 78/100
**Problème résolu :** CV18xx系列 SOC 开源硬件平台
**Comment ça marche :** # 快速入门指南

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
**Spécificité chinoise :** Chinese open-source project
**Équivalent occidental :** Not identified
**Maturité :** Actif (★ 60, 35 forks, mis à jour 2026-08)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/sophgo/sophpi
---
