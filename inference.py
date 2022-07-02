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

_ = utils.load_checkpoint("./logs/G_56000.pth", net_g, None)

if __name__ == "__main__":
    message = '是谁在撩动心弦'

    phonemes = chinese_to_phonemes(message)
    #phonemes = phonemes.replace("^ ", "")

    input_ids = get_text(phonemes, hps)

    with torch.no_grad():
        x_tst = input_ids.unsqueeze(0)
        x_tst_lengths = torch.LongTensor([input_ids.size(0)])
        audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=0, noise_scale_w=0, length_scale=1)[0][0,0].data.cpu().float().numpy()
    save_wav(audio, f"{message}.wav", hps.data.sampling_rate)
    print('推理结束，文件已保存！')