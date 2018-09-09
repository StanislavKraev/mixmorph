from mixmorph.mixmorph import Mixmorph
from mixmorph.server.mm_server import MMServer


def main():
    mixmorph = Mixmorph()
    mm_server = MMServer(mixmorph)
    mm_server.run()


if __name__ == '__main__':
    main()
