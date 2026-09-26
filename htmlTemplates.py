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

# Blue-Purple gradient circle with "U" — for user
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='78' height='78' viewBox='0 0 78 78'>
          <defs>
            <linearGradient id='ugrad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'>
              <stop offset='0%25' style='stop-color:%234f46e5'/>
              <stop offset='100%25' style='stop-color:%237c3aed'/>
            </linearGradient>
          </defs>
          <circle cx='39' cy='39' r='39' fill='url(%23ugrad)'/>
          <text x='39' y='46' font-family='Arial,sans-serif' font-size='26' font-weight='bold' fill='white' text-anchor='middle'>U</text>
        </svg>">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

# Green-Teal gradient circle with "AI" — for bot
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='78' height='78' viewBox='0 0 78 78'>
          <defs>
            <linearGradient id='bgrad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'>
              <stop offset='0%25' style='stop-color:%23059669'/>
              <stop offset='100%25' style='stop-color:%230891b2'/>
            </linearGradient>
          </defs>
          <circle cx='39' cy='39' r='39' fill='url(%23bgrad)'/>
          <text x='39' y='46' font-family='Arial,sans-serif' font-size='22' font-weight='bold' fill='white' text-anchor='middle'>AI</text>
        </svg>">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''