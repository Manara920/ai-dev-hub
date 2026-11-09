"""
Thin wrapper around `airllm` providing a unified interface.
AirLLM requires a full Linux environment (such as proot-distro Ubuntu on Termux)
due to PyTorch and Transformers native dependencies.
"""
import os
import sys
from typing import Any

try:
    import airllm
    AIRLLM_AVAILABLE = True
except ImportError:
    airllm = None
    AIRLLM_AVAILABLE = False

class AirLLMWrapper:
    """Wrapper class for loading and running AirLLM models."""

    def __init__(self, model_path: str):
        in_proot = os.path.exists("/.proot") or os.environ.get("PROOT_TMP_DIR") is not None or os.path.exists("/etc/os-release")
        is_termux = ("com.termux" in os.environ.get("PREFIX", "") or "com.termux" in sys.executable) and not in_proot

        if is_termux and not in_proot:
            raise RuntimeError(
                "AirLLM لا يمكن تشغيله مباشرة في بيئة Termux الأصلية.\n"
                "يرجى تشغيله داخل بيئة Linux (مثل proot-distro login ubuntu) لتوفير دعم PyTorch."
            )

        if not AIRLLM_AVAILABLE:
            raise RuntimeError(
                "مكتبة airllm غير مثبتة في بيئة بايثون الحالية.\n"
                "يمكنك تثبيتها عبر: pip install airllm transformers torch"
            )

        self.model = airllm.AutoModel.from_pretrained(model_path)

    def generate(self, prompt: str, max_new_tokens: int = 256, **kwargs: Any) -> str:
        if not hasattr(self, "model") or self.model is None:
            raise RuntimeError("النموذج غير محمل.")
        input_tokens = self.model.tokenizer(
            [prompt],
            return_tensors="pt",
            return_attention_mask=False,
            truncation=True,
            max_length=2048
        )
        generation_output = self.model.generate(
            input_tokens["input_ids"],
            max_new_tokens=max_new_tokens,
            use_cache=True,
            return_dict_in_generate=True,
            **kwargs
        )
        return self.model.tokenizer.decode(generation_output.sequences[0])
