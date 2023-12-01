import secrets
import string

class Senha:

    def Reload():

        caracteres=(string.ascii_letters+string.digits)

        senhas=''.join([secrets.choice(caracteres) for i in range(20)])

        return senhas

        pass

    pass