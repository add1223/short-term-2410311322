"""首页前端资源(HTML 字符串),避免引入静态目录,保持单文件。"""
INDEX_HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI 文档问答助手</title>
<style>
  :root{
    --c-bg:#f5f7fb; --c-card:#ffffff; --c-ink:#1f2937; --c-muted:#6b7280;
    --c-primary:#2563eb; --c-primary-dark:#1d4ed8; --c-ok:#059669; --c-err:#dc2626;
    --c-border:#e5e7eb; --radius:14px; --shadow:0 4px 18px rgba(15,23,42,.06);
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0;background:var(--c-bg);color:var(--c-ink);
    font-family:-apple-system,"PingFang SC","Microsoft YaHei","Segoe UI",sans-serif;line-height:1.55}
  header{background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;padding:22px 28px}
  header .wrap{max-width:980px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
  header h1{font-size:22px;margin:0;font-weight:600;letter-spacing:.3px}
  header .sub{opacity:.9;font-size:13px;margin-top:2px}
  header .status{background:rgba(255,255,255,.16);border-radius:999px;padding:6px 14px;font-size:13px}
  header .status .dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#4ade80;margin-right:6px;vertical-align:1px}
  main{max-width:980px;margin:22px auto 60px;padding:0 22px;display:grid;gap:18px}
  .row{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  @media(max-width:860px){.row{grid-template-columns:1fr}}
  .card{background:var(--c-card);border-radius:var(--radius);box-shadow:var(--shadow);padding:20px 22px;border:1px solid var(--c-border)}
  .card h2{margin:0 0 6px;font-size:17px;display:flex;align-items:center;gap:8px}
  .card .desc{color:var(--c-muted);font-size:13px;margin-bottom:14px}
  .icon{width:30px;height:30px;border-radius:8px;display:inline-flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:15px}
  .i1{background:#2563eb}.i2{background:#7c3aed}.i3{background:#059669}.i4{background:#f59e0b}
  label{display:block;font-size:13px;color:#374151;margin:10px 0 5px;font-weight:500}
  input[type=text],textarea,select{
    width:100%;padding:9px 12px;border:1px solid var(--c-border);border-radius:10px;font-size:14px;
    font-family:inherit;color:var(--c-ink);background:#fff;outline:none;transition:border .15s
  }
  input:focus,textarea:focus,select:focus{border-color:var(--c-primary);box-shadow:0 0 0 3px rgba(37,99,235,.15)}
  textarea{resize:vertical;min-height:86px}
  button.btn{
    margin-top:12px;width:100%;border:0;background:var(--c-primary);color:#fff;border-radius:10px;
    padding:10px 14px;font-size:14px;font-weight:600;cursor:pointer;transition:background .15s,transform .05s
  }
  button.btn:hover{background:var(--c-primary-dark)}
  button.btn:active{transform:translateY(1px)}
  button.btn.ghost{background:#fff;color:var(--c-primary);border:1px solid var(--c-primary)}
  button.btn.ok{background:var(--c-ok)}
  .two-col{display:grid;grid-template-columns:2fr 1fr;gap:18px}
  @media(max-width:860px){.two-col{grid-template-columns:1fr}}
  .result{margin-top:12px;background:#0f172a;color:#e2e8f0;border-radius:10px;padding:12px 14px;font-size:13px;
    font-family:ui-monospace,"SF Mono",Consolas,"Microsoft YaHei",monospace;white-space:pre-wrap;word-break:break-all;max-height:340px;overflow:auto;display:none}
  .result.show{display:block}
  .tag{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12px;font-weight:600;margin-right:6px}
  .tag.ok{background:#d1fae5;color:var(--c-ok)}.tag.err{background:#fee2e2;color:var(--c-err)}.tag.info{background:#dbeafe;color:var(--c-primary)}
  .quiet{color:var(--c-muted);font-size:12px}
  .ans{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:12px 14px;margin-top:10px;display:none}
  .ans.show{display:block}
  .ans h4{margin:0 0 6px;font-size:14px;color:var(--c-ok)}
  .src{background:#fff;border:1px dashed #86efac;border-radius:8px;padding:8px 10px;margin-top:8px;font-size:13px;color:#14532d}
  .src .sc{float:right;color:var(--c-muted);font-size:12px}
  details{margin-top:8px;background:#f8fafc;border:1px solid var(--c-border);border-radius:10px;padding:10px 12px}
  details summary{cursor:pointer;font-size:13px;color:#334155;font-weight:500}
  .hint{font-size:12px;color:var(--c-muted);margin-top:6px}
  footer{max-width:980px;margin:0 auto 30px;padding:0 22px;color:var(--c-muted);font-size:12px;text-align:center}
  .spinner{display:inline-block;width:12px;height:12px;border:2px solid #fff;border-top-color:transparent;border-radius:50%;animation:spin .8s linear infinite;vertical-align:-2px;margin-right:6px}
  @keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <div>
      <h1>🧠 AI 文档问答助手</h1>
      <div class="sub">上传文档 → 切块+向量检索 → 大模型生成带原文引用的回答 · 本地单机版</div>
    </div>
    <div class="status"><span class="dot"></span><span id="serviceState">服务正常 · 模型 qwen3.5:4b</span></div>
  </div>
</header>

<main>
  <div class="row">
    <section class="card">
      <h2><span class="icon i1">1</span>选择身份登录</h2>
      <p class="desc">editor 可以上传文档和提问，viewer 只能查看和提问。</p>
      <label>身份角色</label>
      <select id="roleSel">
        <option value="editor" selected>editor (可上传+提问)</option>
        <option value="viewer">viewer (仅提问+查看)</option>
      </select>
      <button class="btn" onclick="doLogin()">🔑 登录获取访问凭证</button>
      <div class="result" id="loginOut"></div>
    </section>

    <section class="card">
      <h2><span class="icon i2">2</span>上传文档 (editor)</h2>
      <p class="desc">仅 editor 可用。系统会自动切块，并用 nomic-embed-text 做向量化建索引。</p>
      <label>文档标题</label>
      <input id="docTitle" type="text" placeholder="例如：TDD 讲义第三章">
      <label>文档正文</label>
      <textarea id="docBody" placeholder="把文档正文粘到这里……支持中英文，建议至少 100 字，提问效果更好。&#10;例：&#10;测试驱动开发（TDD）的核心是红绿循环：第一步写一个会失败的测试（红），第二步写刚好通过测试的代码（绿），第三步在测试保护下做重构。"></textarea>
      <button class="btn" onclick="doUpload()">📤 上传文档并建立索引</button>
      <div class="hint">同一内容重复上传会返回 409（防重复）。</div>
      <div class="result" id="uploadOut"></div>
    </section>

    <section class="card">
      <h2><span class="icon i3">3</span>对文档提问</h2>
      <p class="desc">输入问题，系统会从已上传文档里找最相关的片段，再交给大模型生成回答并标注来源。</p>
      <label>文档 ID（上传后会自动填入）</label>
      <input id="docId" type="text" placeholder="如 doc-2410311322-001">
      <label>你的问题</label>
      <textarea id="question" placeholder="例：TDD 的红绿循环指的是什么？"></textarea>
      <button class="btn ok" onclick="doAsk()">💬 生成回答（带引用）</button>
      <div class="hint">与文档无关的问题会返回"未找到相关内容"，不会乱编。</div>
      <div class="ans" id="ansBox">
        <h4 id="ansTitle">回答</h4>
        <div id="ansBody"></div>
        <div id="ansSrcs"></div>
      </div>
      <div class="result" id="askOut"></div>
    </section>
  </div>

  <div class="row">
    <section class="card" style="grid-column:1/-1">
      <h2><span class="icon i4">?</span>查看单个文档信息</h2>
      <p class="desc">输入文档 ID，查看切块数量、字数等基础信息。editor/viewer 都可用。</p>
      <div style="display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap">
        <div style="flex:1;min-width:260px">
          <label>文档 ID</label>
          <input id="getDocId" type="text" placeholder="doc-xxxx-xxx">
        </div>
        <button class="btn ghost" onclick="doGetDoc()" style="width:auto;margin:0;padding:10px 20px">🔍 查询文档</button>
      </div>
      <div class="result" id="getDocOut"></div>
    </section>
  </div>

  <details open>
    <summary>📘 快速上手演示（点我折叠/展开）</summary>
    <ol style="margin:10px 0 0 20px;padding:0;font-size:13px;color:#374151;line-height:1.9">
      <li>点左上方卡片的 <b>"登录获取访问凭证"</b>（默认 editor 角色）→ 右侧会显示 token（已自动保存到本机，不用手复制）。</li>
      <li>中间卡片填入标题和一段正文 → <b>"上传文档并建立索引"</b> → 返回 doc_id（会自动填到右边提问卡片）。</li>
      <li>右边卡片输入问题 → <b>"生成回答"</b> → 下方会显示：回答正文 + has_answer（是/否） + 引用的原文片段 + 相似度分。</li>
    </ol>
  </details>
</main>

<footer>© solo-2410311322-ai-doc-qa-assistant · 提交期 M 项目 · FastAPI + Ollama（qwen3.5:4b / nomic-embed-text）</footer>

<script>
  const $ = id => document.getElementById(id);
  const TOKEN_KEY = 'qa_assistant_token';
  let TOKEN = localStorage.getItem(TOKEN_KEY) || '';
  if(TOKEN) $('serviceState').textContent = '已登录 · 模型 qwen3.5:4b';

  function setBtnLoading(btn, loadingText){
    if(loadingText){
      btn.__orig = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner"></span>' + loadingText;
    }else{
      btn.disabled = false;
      btn.innerHTML = btn.__orig || btn.innerHTML;
    }
  }
  function show(elId, text){
    const el = $(elId);
    el.textContent = text;
    el.classList.add('show');
  }
  async function api(method, path, body){
    const opts = {method, headers:{'Content-Type':'application/json'}};
    if(TOKEN) opts.headers['Authorization'] = 'Bearer ' + TOKEN;
    if(body) opts.body = JSON.stringify(body);
    const r = await fetch(path, opts);
    let data; try { data = await r.json(); } catch(e){ data = {raw: await r.text()}; }
    return {status: r.status, data};
  }

  async function doLogin(){
    const role = $('roleSel').value;
    setBtnLoading(event.target, '登录中…');
    try{
      const {status, data} = await api('POST','/login',{role});
      let html = '<span class="tag '+(status===200?'ok':'err')+'">'+status+'</span>返回：\n'+JSON.stringify(data,null,2);
      show('loginOut', html);
      if(status===200){
        TOKEN = data.token; localStorage.setItem(TOKEN_KEY, TOKEN);
        $('serviceState').textContent = (data.role==='editor'?'editor':'viewer') + ' 已登录 · 模型 qwen3.5:4b';
      }
    }finally{ setBtnLoading(event.target); }
  }

  async function doUpload(){
    const title = $('docTitle').value.trim();
    const content = $('docBody').value.trim();
    if(!title || !content){ show('uploadOut','<span class="tag err">校验</span>标题和正文都不能为空。'); return; }
    if(!TOKEN){ show('uploadOut','<span class="tag err">未登录</span>请先点左上方登录获取凭证。'); return; }
    setBtnLoading(event.target, '切块+向量化中…（首次调用模型需几秒）');
    try{
      const {status, data} = await api('POST','/documents',{title,content});
      let html = '<span class="tag '+(status===201?'ok':'err')+'">'+status+'</span>返回：\n'+JSON.stringify(data,null,2);
      show('uploadOut', html);
      if(status===201 && data.doc_id){
        $('docId').value = data.doc_id;
        $('getDocId').value = data.doc_id;
      }
    }finally{ setBtnLoading(event.target); }
  }

  async function doAsk(){
    const docId = $('docId').value.trim();
    const q = $('question').value.trim();
    if(!docId){ show('askOut','<span class="tag err">缺少 doc_id</span>请先上传文档或手动填文档 ID。'); return; }
    if(!q){ show('askOut','<span class="tag err">空问题</span>请输入问题。'); return; }
    if(!TOKEN){ show('askOut','<span class="tag err">未登录</span>请先点左上方登录。'); return; }
    $('ansBox').classList.remove('show');
    setBtnLoading(event.target, '检索+生成中…（真实大模型调用，约5-15秒）');
    try{
      const {status, data} = await api('POST','/documents/'+encodeURIComponent(docId)+'/ask',{question: q});
      let html = '<span class="tag '+(status===200?'ok':'err')+'">'+status+'</span>返回：\n'+JSON.stringify(data,null,2);
      show('askOut', html);
      if(status===200 && typeof data==='object'){
        $('ansBox').classList.add('show');
        const has = !!data.has_answer;
        $('ansTitle').innerHTML = (has?'✅ 找到相关内容并回答':'⚠️ 未找到相关内容（has_answer=false）')
          + (has?'':' — 请换个说法或确认问题是否与文档匹配。');
        $('ansBody').innerHTML = data.answer || '';
        const srcs = data.sources || [];
        $('ansSrcs').innerHTML = srcs.length
          ? '<div style="margin-top:8px;font-weight:600;color:#166534;font-size:13px">📎 引用来源（'+srcs.length+' 段）：</div>'
            + srcs.map(s => '<div class="src"><span class="sc">score '+(Number(s.score||0).toFixed(3))+'</span><b>#'+s.chunk_index+'</b> '+(s.text||'')+'</div>').join('')
          : '<div class="quiet" style="margin-top:6px">没有返回引用片段（has_answer=false 时通常如此）。</div>';
      }
    }finally{ setBtnLoading(event.target); }
  }

  async function doGetDoc(){
    const docId = $('getDocId').value.trim();
    if(!docId){ show('getDocOut','<span class="tag err">缺少 doc_id</span>'); return; }
    if(!TOKEN){ show('getDocOut','<span class="tag err">未登录</span>'); return; }
    const {status, data} = await api('GET','/documents/'+encodeURIComponent(docId));
    show('getDocOut', '<span class="tag '+(status===200?'ok':'err')+'">'+status+'</span>返回：\n'+JSON.stringify(data,null,2));
  }
</script>
</body>
</html>
'''