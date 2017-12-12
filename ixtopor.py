
import time

# Flags binárias - para que mais de uma direção possa estar ativa ao mesmo tempo.
# Para verificar se uma flag está ativa, usamos o mod:
# if self.flags_linear % flag_right:
#     (incrementar eixo x...)

flag_right, flag_up, flag_left, flag_down = 0b0001, 0b0010, 0b0100, 0b1000
flag_claw_cw, flag_claw_ccw, flag_base_cw, flag_base_ccw = 0b0001, 0b0010, 0b0100, 0b1000

class Ixtopor:

    def __init__(self, ui):
        self.ui = ui
        self.temperature = 0
        self.linearSpeed, self.baseSpeed, self.clawSpeed = 0, 0, 0
        self.maxLinearSpeed, self.maxBaseSpeed, self.maxClawSpeed = 120, 200, 200
        self.flags_linear = 0b0000
        self.flags_rotation = 0b0000

        self.commands = []  # para código
        self.commands_being_played = []

    def updateLinearSpeed(self, percentage):
        self.linearSpeed = round(0.01 * percentage * self.maxLinearSpeed)
        self.ui.labelLinearSpeed.setText("{} mm/min".format(self.linearSpeed))

    def updateBaseSpeed(self, percentage):
        self.baseSpeed = round(0.01 * percentage * self.maxBaseSpeed)
        self.ui.labelBaseSpeed.setText("{} º/min".format(self.baseSpeed))

    def updateClawSpeed(self, percentage):
        self.clawSpeed = round(0.01 * percentage * self.maxClawSpeed)
        self.ui.labelClawSpeed.setText("{} º/min".format(self.clawSpeed))

    def updateTemperature(self, percentage):
        self.temperature = percentage
        self.ui.labelTemperature.setText("{}%".format(self.temperature))

    def set_flag_linear(self, flag):
        self.flags_linear |= flag

    def clear_flag_linear(self, flag):
        self.flags_linear &= ~flag

    def set_flag_rotation(self, flag):
        self.flags_rotation |= flag

    def clear_flag_rotation(self, flag):
        self.flags_rotation &= ~flag

    def parse_commands(self, text: str):
        self.commands = []
        commands_temp = []
        named_subroutines = []
        errors = []
        lower_text = text.lower()
        for i, line in enumerate(lower_text.split('\n')):

            if line == '':
                continue

            parts = line.rstrip(' ').split(' ')

            if parts[0] not in ['mov', 'rot', 'do', 'vel', 'esr', 'fsr'] and not parts[0].endswith(':'):
                errors.append('[linha {}] Função desconhecida: {}'.format(i+1, parts[0]))

            if (parts[0] in ['mov', 'rot', 'vel'] and len(parts) != 3)\
                    or (parts[0] in ['vel', 'esr', 'fsr'] and len(parts) != 2)\
                    or (parts[0] in ['do'] and len(parts) != 1):
                errors.append('[linha {}] Número errado de argumentos para função {}'.format(i+1, parts[0]))

            if parts[0].endswith(':') and \
                    (len(parts) != 1 or len(parts[0]) == 1 or parts[0][:-1] in ['mov', 'rot', 'do', 'vel', 'esr', 'fsr']):
                errors.append('[linha {}] Subrotina inválida'.format(i+1))

            if parts[0].endswith(':'):
                print(named_subroutines)
                if parts[0][:-1] in named_subroutines:
                    errors.append('[linha {}] Subrotina duplicada: {}'.format(i+1, parts[0][:-1]))
                else:
                    named_subroutines.append(parts[0][:-1])

            if parts[0] == 'fsr' and parts in commands_temp:
                errors.append('[linha {}] Fim de subrotina duplicado: {}'.format(i+1, parts[1]))

            try:
                if parts[0] in ['esr', 'fsr']:
                    if parts[1] not in named_subroutines:
                        errors.append('[linha {}] Subrotina desconhecida: {}'.format(i+1, parts[1]))

                if parts[0] == 'mov':
                    if parts[1] not in ['x', 'y']:
                        errors.append('[linha {}] Eixo inválido para função mov: {}'.format(i+1, parts[1]))
                    try:
                        parts[2] = int(parts[2])
                    except ValueError:
                        errors.append('[linha {}] Valor precisa ser número inteiro: {}'.format(i + 1, parts[1]))

                elif parts[0] == 'rot':
                    if parts[1] not in ['b', 'g']:
                        errors.append('[linha {}] Eixo inválido para função rot: {}'.format(i+1, parts[1]))
                    try:
                        parts[2] = int(parts[2])
                    except ValueError:
                        errors.append('[linha {}] Valor precisa ser número inteiro: {}'.format(i + 1, parts[1]))

                elif parts[0] == 'vel':
                    if parts[1] not in ['b', 'g', 'xy']:
                        errors.append('[linha {}] Eixo inválido para função vel: {}'.format(i+1, parts[1]))
                    try:
                        parts[2] = int(parts[2])
                    except ValueError:
                        errors.append('[linha {}] Valor precisa ser número inteiro: {}'.format(i + 1, parts[1]))
            except IndexError:
                pass

            commands_temp.append((parts, i))

        def assert_subroutines_end(cmds, append_errors):
            cmds_noline = [cmd[0] for cmd in cmds]
            for i, cmd in enumerate(cmds_noline):
                if cmd[0].endswith(':'):
                    if ['fsr', cmd[0][:-1]] not in cmds_noline[i:]:
                        if append_errors:
                            errors.append('[linha {}] Subrotina sem fim: {}'.format(cmds[i][1] + 1, cmd[0][:-1]))
                        return False
            return True

        assert_subroutines_end(commands_temp, True)

        commands_temp_noline = [command[0] for command in commands_temp]
        for i, command in enumerate(commands_temp_noline):
            if command[0].endswith(':'):
                print('x', ['fsr', command[0][:-1]], commands_temp_noline[i:])
                if ['fsr', command[0][:-1]] in commands_temp_noline[i:]:
                    fsr = commands_temp_noline.index(['fsr', command[0][:-1]], i) + 1
                    if not assert_subroutines_end(commands_temp[i:fsr], False):
                        errors.append('[linha {}] Erro de fluxo de subrotina: {}'.format(commands_temp[i][1] + 1, command[0][:-1]))
                        break
                    print(commands_temp_noline)
                    if ['esr', command[0][:-1]] in commands_temp_noline[i:fsr]:
                        errors.append('[linha {}] Subrotina dentro de si mesma: {}'.format(
                            commands_temp[i:fsr].index(['esr', command[0][:-1]]) + commands_temp[i][1] + 1 + 1, command[0][:-1]))

        if not errors:
            self.commands = commands_temp
            return ['Ok']
        else:
            return errors

    def play_commands(self):
        self.ui.textEdit.setEnabled(False)
        # self.commands_being_played = self.commands
        for i, command in enumerate(self.commands):
            print(command)
            time.sleep(1)  # melhoria: tornar espera por comando não-blocante
            self.ui.progressBar.setValue(round(100*(i+1))/len(self.commands))
        self.ui.textEdit.setEnabled(True)
