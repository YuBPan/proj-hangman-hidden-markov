

class GameClient():

    def create_game(self, s, total_number):
        self.s = list(s.lower())
        self.total_number = total_number
        self.remain_number = total_number
        self.ongoing_str = []
        self.unsolved = 0

        for c in self.s:
            if c.isalpha() or c == " ":
                self.ongoing_str.append("_" if c.isalpha() else c)
                self.unsolved += 1 if c.isalpha() else 0
            else:
                self.ongoing_str.append(" ")

        return {"str" : "".join(self.ongoing_str),
                "remain" : self.remain_number,
                "status" : "ONGOING"}

    def guess(self, letter):
        if self.remain_number <= 0:
            return {"str" : "".join(self.ongoing_str),
                    "remain" : self.remain_number,
                    "status": "LOSE"}

        if letter != '':
            revealed = False
            for i in range(len(self.ongoing_str)):
                if self.ongoing_str[i] == "_" and self.s[i] == letter.lower():
                    self.ongoing_str[i] = letter.lower()
                    self.unsolved -= 1
                    revealed = True
            if not revealed:
                self.remain_number -= 1
        else:
            self.remain_number -= 1

        if self.unsolved == 0:
            status = "WIN"
            return {"str" : "".join(self.ongoing_str),
                    "remain" : self.remain_number,
                    "status" : status,
                    "cost" : (self.total_number - self.remain_number)}
        else:
            status = "LOSE" if self.remain_number == 0 else "ONGOING"
            return {"str" : "".join(self.ongoing_str),
                    "remain" : self.remain_number,
                    "status": status}
