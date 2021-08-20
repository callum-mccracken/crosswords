from ipxword import Grid, IPXWordGenerator
import random


N = 7
N_black = random.randint(0, N*N)
black_squares = [divmod(ele, N) for ele in random.sample(range((N) * (N)), N_black)]

while True:
    try:
        G = Grid(N, blacksq=black_squares)
        ipx = IPXWordGenerator(G, numk=3000, wordfile='UKACD18plus.txt', verbose=True)
        ipx.build(verbose=True)
        break
    except ValueError:
        N_black = random.randint(0, N*N)
        black_squares = [divmod(ele, N) for ele in random.sample(range((N) * (N)), N_black)]
        print('failed building, trying again')

print('done')
ipx.get_puzzle()

