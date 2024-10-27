from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import soundfile as sf
import time
config = XttsConfig()
config.load_json("./XTTS-v2/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="./XTTS-v2/", eval=True)
start_time = time.time()
outputs = model.synthesize(
    "Таблетка не найдена в базе",
    config,
    speaker_wav="./XTTS-v2/samples/en_sample.wav",
    gpt_cond_len=3,
    language="ru",
)
end_time = time.time() 
execution_time = end_time - start_time
output_path = "./main/not_found.wav"
sf.write(output_path, outputs['wav'], 22050)
print(f"Файл сохранен как {output_path}")
print(execution_time)