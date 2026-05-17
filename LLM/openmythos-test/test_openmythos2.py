# test_openmythos2.py
from open_mythos.main import OpenMythos, MythosConfig
import torch

cfg = MythosConfig()
model = OpenMythos(cfg)
model.eval()

# トークナイザーなしで簡易テスト
with torch.no_grad():
    input_ids = torch.randint(0, cfg.vocab_size, (1, 5))
    output = model.generate(input_ids, max_new_tokens=50)
    print(f"入力: {input_ids.tolist()}")
    print(f"出力: {output.tolist()}")
    print(f"生成トークン数: {output.shape[1] - input_ids.shape[1]}")
