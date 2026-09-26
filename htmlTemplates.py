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

# Futuristic Siri-style aurora ring — no text, dark center, electric color halo
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160' viewBox='0 0 160 160'><defs><radialGradient id='bg' cx='50%25' cy='50%25' r='50%25'><stop offset='0%25' style='stop-color:%23070720'/><stop offset='100%25' style='stop-color:%23020210'/></radialGradient><filter id='f1'><feGaussianBlur stdDeviation='13'/></filter><filter id='f2'><feGaussianBlur stdDeviation='18'/></filter><clipPath id='cl'><circle cx='80' cy='80' r='80'/></clipPath><radialGradient id='cg' cx='50%25' cy='50%25' r='50%25'><stop offset='0%25' style='stop-color:%23060618;stop-opacity:1'/><stop offset='72%25' style='stop-color:%23060618;stop-opacity:0.96'/><stop offset='100%25' style='stop-color:%23060618;stop-opacity:0'/></radialGradient></defs><circle cx='80' cy='80' r='80' fill='url(%23bg)'/><g clip-path='url(%23cl)'><ellipse cx='138' cy='75' rx='52' ry='40' fill='%2300ccff' opacity='0.95' filter='url(%23f1)'/><ellipse cx='80' cy='20' rx='50' ry='38' fill='%237c3aed' opacity='0.90' filter='url(%23f1)'/><ellipse cx='20' cy='75' rx='52' ry='40' fill='%23ff0080' opacity='0.90' filter='url(%23f1)'/><ellipse cx='80' cy='142' rx='50' ry='38' fill='%23ff6a00' opacity='0.88' filter='url(%23f1)'/><ellipse cx='132' cy='22' rx='44' ry='34' fill='%2306d6d4' opacity='0.82' filter='url(%23f2)'/><ellipse cx='22' cy='135' rx='44' ry='34' fill='%23d026d3' opacity='0.78' filter='url(%23f2)'/><ellipse cx='132' cy='135' rx='44' ry='34' fill='%23fb923c' opacity='0.72' filter='url(%23f2)'/><ellipse cx='22' cy='22' rx='44' ry='34' fill='%236366f1' opacity='0.72' filter='url(%23f2)'/></g><circle cx='80' cy='80' r='54' fill='url(%23cg)'/><circle cx='80' cy='80' r='64' fill='none' stroke='white' stroke-width='1' opacity='0.18'/><circle cx='80' cy='80' r='53' fill='none' stroke='%2300ccff' stroke-width='0.8' opacity='0.25'/></svg>" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
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