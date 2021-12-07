import model as md
import data_handler as dh
import data_handler2 as dh2
import train as tr
import torch

if __name__ == '__main__':
    _, testloader = tr.load_data()
    model = md.Network()
    model.load_state_dict(torch.load('./02. MLP Regression/model.pth'))
    model.eval()
    with torch.no_grad():
        for x_test, y_test in iter(testloader):
            x_test, y_test = x_test.float(), y_test.float()

            outputs_test = model(x_test)
