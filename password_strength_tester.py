import wx
import re
import math

class PasswordStrengthTester(wx.Frame):
    def __init__(self, parent, title):
        super(PasswordStrengthTester, self).__init__(parent, title=title, size=(400, 300))
        self.SetBackgroundColour("#1A1A1A")

        # Create panel and sizer
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Label
        self.label = wx.StaticText(panel, label="Enter your password:")
        self.label.SetForegroundColour("#00FF00")
        self.label.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        sizer.Add(self.label, 0, wx.ALL | wx.CENTER, 10)

        # Password entry
        self.password_entry = wx.TextCtrl(panel, style=wx.TE_PASSWORD, size=(300, 30))
        self.password_entry.SetForegroundColour("#00FF00")
        self.password_entry.SetBackgroundColour("#2A2A2A")
        sizer.Add(self.password_entry, 0, wx.ALL | wx.CENTER, 10)

        # Check button
        self.check_button = wx.Button(panel, label="Check Password")
        self.check_button.SetBackgroundColour("#00FF00")
        self.check_button.SetForegroundColour("#1A1A1A")
        self.check_button.Bind(wx.EVT_BUTTON, self.on_check_password)
        sizer.Add(self.check_button, 0, wx.ALL | wx.CENTER, 10)

        # Result text
        self.result_text = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER)
        self.result_text.SetForegroundColour("#00FF00")
        self.result_text.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        sizer.Add(self.result_text, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(sizer)
        self.Centre()
        self.Show()

    def on_check_password(self, event):
        password = self.password_entry.GetValue()
        score = 0
        feedback = []

        # Check length
        if len(password) < 8:
            feedback.append("Password should be at least 8 characters long.")
        else:
            score += min(len(password) * 4, 40)

        # Check for uppercase letters
        if re.search(r"[A-Z]", password):
            score += 15
        else:
            feedback.append("Add uppercase letters (A-Z).")

        # Check for lowercase letters
        if re.search(r"[a-z]", password):
            score += 15
        else:
            feedback.append("Add lowercase letters (a-z).")

        # Check for numbers
        if re.search(r"\d", password):
            score += 15
        else:
            feedback.append("Add numbers (0-9).")

        # Check for special characters
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 15
        else:
            feedback.append("Add special characters (e.g., !@#$%).")

        # Estimate crack time
        crack_time = self.estimate_crack_time(password)

        # Determine strength
        strength = "Very Weak"
        if score >= 80:
            strength = "Strong"
        elif score >= 50:
            strength = "Moderate"
        elif score >= 30:
            strength = "Weak"

        # Prepare result
        result_text = f"Password Strength: {strength}\nScore: {score}/100\nEstimated Crack Time: {crack_time}\n\nFeedback:\n"
        if feedback:
            result_text += "\n".join(feedback)
        else:
            result_text += "Great job! Your password is strong."

        self.result_text.SetLabel(result_text)

    def estimate_crack_time(self, password):
        guesses_per_second = 10_000_000_000
        charset_size = 0

        if re.search(r"[a-z]", password):
            charset_size += 26
        if re.search(r"[A-Z]", password):
            charset_size += 26
        if re.search(r"\d", password):
            charset_size += 10
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            charset_size += 32

        combinations = charset_size ** len(password)
        seconds = combinations / guesses_per_second

        if seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds / 60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds / 3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds / 86400)} days"
        else:
            return f"{int(seconds / 31536000)} years"

if __name__ == "__main__":
    app = wx.App()
    frame = PasswordStrengthTester(None, "Password Strength Tester by alirezabytes")
    app.MainLoop()