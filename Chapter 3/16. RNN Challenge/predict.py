import helper_functions as hp
import train as tr
import models as md
import matplotlib.pyplot as plt
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
input_lang, output_lang, pairs = hp.prepareData('eng', 'fra', True)
hidden_size = 256
encoder1 = md.EncoderLSTM(input_lang.n_words, hidden_size, 2).to(device)
attn_decoder1 = md.AttnDecoderLSTM(hidden_size, output_lang.n_words, 2, dropout_p=0.1).to(device)

tr.trainIters(encoder1, attn_decoder1, 75000, print_every=5000)



# output_words, attentions = tr.evaluate(encoder1, attn_decoder1, "je suis trop froid .")
# plt.matshow(attentions.numpy())

# tr.evaluateAndShowAttention("elle a cinq ans de moins que moi .")
# tr.evaluateAndShowAttention("elle est trop petit .")
# tr.evaluateAndShowAttention("je ne crains pas de mourir .")
# tr.evaluateAndShowAttention("c est un jeune directeur plein de talent .")
