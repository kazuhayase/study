# test_openmythos.py
from open_mythos.main import OpenMythos, MythosConfig

# 最小構成で起動
cfg = MythosConfig()
model = OpenMythos(cfg)

print("モデル構成:")
print(f"  パラメータ数: {sum(p.numel() for p in model.parameters()):,}")

# テキスト生成
import torch
input_ids = torch.randint(0, 1000, (1, 10))
output = model.generate(input_ids, max_new_tokens=20)
print(f"  出力トークン数: {output.shape}")
print("動作確認OK！")
