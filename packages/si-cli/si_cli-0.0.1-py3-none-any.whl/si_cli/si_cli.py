#104 = 10 + 4^10
import click
from si_prefix import si_format, si_parse

@click.group()
def cli():
    pass

def from3dig(number, cap=False):
    digits = [int(number / 10), number % 10]
    conv = digits[0] * 10**digits[1]
    if cap:
        conv = conv / 1000000000000
    return si_format(conv , precision=0)+ ('f' if cap else '')

def to3dig(number, cap=False):
    number = si_parse(number)
    if cap:
        number = number * 1000000000000
    length = len(str(round(number))) - 2 
    return round(number / 10**length * 10 + length)

@cli.command()
@click.argument('number', type=click.STRING)
def to(number):
    """from normal to si(100k>104)"""
    if 'u' in number:
        number = number.replace('u','µ')
    if number.endswith('f'):
        # cap
        number = number.replace('f','')
        print(to3dig(number, cap=True))
    else:
        print(to3dig(number))

@cli.command(name='from')
@click.argument('number', type=click.INT)
@click.option('--cap', is_flag=True)
def _from(number, cap):
    """from si to normal(104>100k)"""
    if len(str(number)) != 3:
        exit("number should have 3 digits")
    print(from3dig(number, cap))

if __name__ == '__main__':
    cli()
