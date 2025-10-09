document.addEventListener('DOMContentLoaded',function(){
  console.log('chat.js loaded');
  var input=document.getElementById('chatInput');
  var send=document.getElementById('sendBtn');
  var messages=document.getElementById('messages');

  function addMessage(text,me){
    if(!text) return;
    var row=document.createElement('div');
    row.className='msg-row';
    if(me){
      row.classList.add('me-row');
    } else {
      row.classList.add('you-row');
    }

    var avatar=document.createElement('div');
    avatar.className='msg-avatar';

    var bubbleWrap=document.createElement('div');
    bubbleWrap.className='msg-bubble';

    var bubble=document.createElement('div');
    bubble.className='msg'+(me? ' me':' you');
    bubble.textContent=text;

    var time=document.createElement('span');
    time.className='msg-time';
    var d=new Date();
    time.textContent = d.getHours().toString().padStart(2,'0') + ':' + d.getMinutes().toString().padStart(2,'0');

    bubbleWrap.appendChild(bubble);

    if(me){
      row.appendChild(avatar);
      row.appendChild(bubbleWrap);
      row.appendChild(time);
    } else {
      row.appendChild(time);
      row.appendChild(bubbleWrap);
      row.appendChild(avatar);
    }

    messages.appendChild(row);
    messages.scrollTop=messages.scrollHeight;
  }

  var GEMINI_API_KEY = (window && window.GEMINI_API_KEY) ? window.GEMINI_API_KEY : '';

  function callGeminiPrompt(prompt){
    return fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: prompt })
    }).then(function(res){ return res.json(); }).then(function(data){
      console.log('chat proxy response', data);
      if(data && data.ok && data.reply) return data.reply;
      if(data && data.reply) return data.reply;
      if(data && data.candidates && data.candidates.length>0){
        var candidate = data.candidates[0];
        if(candidate && candidate.content && candidate.content.length>0 && candidate.content[0].text) return candidate.content[0].text;
      }
      if(data && data.error) throw new Error(data.error);
      return JSON.stringify(data);
    });
  }

  function sendMessage(){
    var text = input.value.trim();
    if(!text) return;
    addMessage(text, true);
    input.value = '';
    input.focus();
    callGeminiPrompt(text).then(function(reply){
      console.log('gemini reply:', reply);
      addMessage(reply, false);
    }).catch(function(err){
      console.error('gemini call failed:', err);
      addMessage('Error contacting Gemini.', false);
    });
  }

  send.addEventListener('click', sendMessage);
  input.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); sendMessage(); } });
});
