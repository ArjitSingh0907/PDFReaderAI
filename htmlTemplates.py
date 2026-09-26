css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

# Siri-style aurora glow AI avatar
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160' viewBox='0 0 160 160'><defs><radialGradient id='bg' cx='50%25' cy='50%25' r='50%25'><stop offset='0%25' style='stop-color:%230f0c29'/><stop offset='100%25' style='stop-color:%23050510'/></radialGradient><filter id='f1'><feGaussianBlur stdDeviation='15'/></filter><filter id='f2'><feGaussianBlur stdDeviation='20'/></filter><filter id='f3'><feGaussianBlur stdDeviation='10'/></filter><clipPath id='cl'><circle cx='80' cy='80' r='80'/></clipPath></defs><circle cx='80' cy='80' r='80' fill='url(%23bg)'/><g clip-path='url(%23cl)'><ellipse cx='40' cy='100' rx='70' ry='58' fill='%234f46e5' opacity='0.80' filter='url(%23f1)'/><ellipse cx='120' cy='60' rx='65' ry='52' fill='%23ec4899' opacity='0.70' filter='url(%23f1)'/><ellipse cx='80' cy='135' rx='60' ry='48' fill='%2306b6d4' opacity='0.75' filter='url(%23f2)'/><ellipse cx='25' cy='38' rx='52' ry='42' fill='%238b5cf6' opacity='0.60' filter='url(%23f1)'/><ellipse cx='135' cy='125' rx='48' ry='42' fill='%23f59e0b' opacity='0.50' filter='url(%23f2)'/><ellipse cx='80' cy='75' rx='32' ry='28' fill='%23c026d3' opacity='0.40' filter='url(%23f3)'/><ellipse cx='60' cy='55' rx='28' ry='22' fill='%2322d3ee' opacity='0.35' filter='url(%23f3)'/></g><text x='80' y='92' font-family='Arial,sans-serif' font-size='36' font-weight='bold' fill='white' text-anchor='middle' opacity='0.97' style='letter-spacing:3'>AI</text></svg>" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

# Dotted person silhouette on deep navy background
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160' viewBox='0 0 160 160'><defs><radialGradient id='ubg' cx='40%25' cy='35%25' r='65%25'><stop offset='0%25' style='stop-color:%231e3a8a'/><stop offset='100%25' style='stop-color:%230f172a'/></radialGradient><pattern id='dp' x='0' y='0' width='10' height='10' patternUnits='userSpaceOnUse'><circle cx='5' cy='5' r='3' fill='white' opacity='0.90'/></pattern><clipPath id='ch'><circle cx='80' cy='55' r='27'/></clipPath><clipPath id='cb'><ellipse cx='80' cy='116' rx='40' ry='26'/></clipPath></defs><circle cx='80' cy='80' r='80' fill='url(%23ubg)'/><circle cx='80' cy='55' r='27' fill='url(%23dp)' clip-path='url(%23ch)'/><ellipse cx='80' cy='116' rx='40' ry='26' fill='url(%23dp)' clip-path='url(%23cb)'/></svg>" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''