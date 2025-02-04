import torch
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text.utils_ch import chinese_to_phonemes,get_text,save_wav



# define model and load checkpoint
hps = utils.get_hparams_from_file("./configs/baker_base.json")

net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model)
_ = net_g.eval()

_ = utils.load_checkpoint("./logs/G_74000.pth", net_g, None)

if __name__ == "__main__":
    message = '那一年，发生了前所未见的牛瘟，每天都要出现一些大牛和小牛的尸体'

    phonemes = chinese_to_phonemes(message)
    #phonemes = phonemes.replace("^ ", "")

    input_ids = get_text(phonemes, hps)

    with torch.no_grad():
        x_tst = input_ids.unsqueeze(0)
        x_tst_lengths = torch.LongTensor([input_ids.size(0)])
        audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=0.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
    save_wav(audio, f"wav/{message}.wav", hps.data.sampling_rate)
    print('推理结束，文件已保存！')