const API = "http://127.0.0.1:8000";

function showToast(message, type="success"){

    const container = document.getElementById("toastContainer");

    const toast = document.createElement("div");

    toast.className = `toast ${type}`;

    toast.innerHTML = message;

    container.appendChild(toast);

    setTimeout(()=>{

        toast.style.animation="fadeOut .4s forwards";

        setTimeout(()=>{

            toast.remove();

        },400);

    },3000);

}

function animateCounter(id, endValue, duration = 800) {

    const element = document.getElementById(id);

    const startValue = parseInt(element.innerText) || 0;

    const range = endValue - startValue;

    if (range === 0) return;

    let startTime = null;

    function update(currentTime) {

        if (!startTime)
            startTime = currentTime;

        const progress = Math.min(
            (currentTime - startTime) / duration,
            1
        );

        const value = Math.floor(
            startValue + range * progress
        );

        element.innerText = value;
        
        element.classList.add("counter-update");
        setTimeout(() => {
            element.classList.remove("counter-update");
        }, 400);

        if (progress < 1)
            requestAnimationFrame(update);

    }

    requestAnimationFrame(update);

}

async function loadStatus() {

    const r = await fetch(API + "/status");

    const d = await r.json();

    animateCounter("vectorCount",d.vectors);
    animateCounter("docCount",d.vectors);
    document.getElementById("latency").textContent = "0 ms";
}

async function insertDoc() {

    const insertBtn = document.getElementById("insertBtn");

    const titleInput = document.getElementById("title");
    const textInput = document.getElementById("text");

    const title = titleInput.value.trim();
    const text = textInput.value.trim();

    // Validation
    if (!title || !text) {

        showToast("❌ Please enter both title and document text.", "error");
        return;

    }

    try {

        // Disable button
        insertBtn.disabled = true;
        insertBtn.innerHTML = "🧠 Generating Embedding...";

        // Small delay for animation
        await new Promise(resolve => setTimeout(resolve, 500));

        insertBtn.innerHTML = "💾 Saving Document...";

        await fetch(API + "/insert", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title,
                text
            })

        });

        insertBtn.innerHTML = "✅ Inserted";

        showToast("✅ Document inserted successfully!", "success");

        // Clear input fields
        titleInput.value = "";
        textInput.value = "";

        // Focus title again
        titleInput.focus();

        // Refresh UI
        loadStatus();
        drawVectors();
        loadRecentDocs();

        // Keep success message visible
        await new Promise(resolve => setTimeout(resolve, 700));

        insertBtn.innerHTML = "➕ Insert Document";
        insertBtn.disabled = false;

    }

    catch (err) {

        console.error(err);

        insertBtn.innerHTML = "➕ Insert Document";
        insertBtn.disabled = false;

        showToast("❌ Failed to connect to server.", "error");

    }

}

async function searchDoc(){

    const query=document.getElementById("query").value.trim();

    if(!query){

        showToast("⚠ Enter a search query.","error");

        return;

    }

    const start=performance.now();

    const r=await fetch(API+"/search",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            query
        })

    });

    const end=performance.now();

    document.getElementById("latency").innerHTML=
    (end-start).toFixed(1)+" ms";

    const data=await r.json();

    let html="";

    if(data.length===0){

        html=`
        <div class="empty-results">

            No similar documents found.

        </div>
        `;

    }

    data.forEach(doc=>{

        const similarity=((1-doc.score)*100).toFixed(2);

        html+=`

        <div class="result-card">

            <div class="result-title">

                📄 ${doc.metadata.title}

            </div>

            <div class="result-score">

                Similarity ${similarity}%

            </div>

            <div class="result-text">

                ${doc.metadata.text}

            </div>

        </div>

        `;

    });

    document.getElementById("results").innerHTML=html;

}

async function askAI(){

    const query = document.getElementById("query").value.trim();

    if(!query){

        showToast("⚠ Please enter a question.","error");
        return;

    }

    const btn = document.getElementById("askBtn");

    btn.disabled = true;
    btn.innerHTML = "🧠 Thinking...";

    try{

        const start = performance.now();

        const r = await fetch(API + "/ask",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                question:query

            })

        });

        const end = performance.now();

        document.getElementById("latency").innerHTML =
        (end-start).toFixed(1) + " ms";

        const data = await r.json();

        let html = `

        <div class="ai-answer">

            <h3>🤖 AI Answer</h3>

            <p>${data.answer}</p>

            <hr>

            <h4>📚 Sources</h4>

        `;

        data.sources.forEach(src=>{

            html += `

            <div class="source-card">

                <b>${src.title}</b>

                <span>${src.score}%</span>

            </div>

            `;

        });

        html += "</div>";

        document.getElementById("results").innerHTML = html;

        btn.innerHTML = "✨ Ask AI";

        btn.disabled = false;

    }

    catch(err){

        console.error(err);

        btn.innerHTML = "✨ Ask AI";

        btn.disabled = false;

        showToast("❌ AI request failed.","error");

    }

}

async function uploadPDF(event) {

    const file = event.target.files[0];

    if (!file) return;

    const btn = document.getElementById("uploadPdfBtn");

    btn.disabled = true;
    btn.innerHTML = "📖 Reading PDF...";

    const formData = new FormData();

    formData.append("file", file);

    try {

        await new Promise(r => setTimeout(r, 400));

        btn.innerHTML = "✂️ Chunking...";

        await new Promise(r => setTimeout(r, 400));

        btn.innerHTML = "🧠 Generating Embeddings...";

        const response = await fetch(API + "/upload_pdf", {

            method: "POST",

            body: formData

        });

        if (!response.ok) {

            throw new Error("Upload failed");

        }

        const data = await response.json();

        btn.innerHTML = `✅ ${data.chunks} Chunks Indexed`;

        showToast(
            `✅ ${data.filename} uploaded successfully`,
            "success"
        );

        // Refresh dashboard
        await loadStatus();
        drawVectors();
        loadRecentDocs();

    } catch (err) {

        console.error(err);

        showToast(
            "❌ Failed to upload PDF",
            "error"
        );

    }

    setTimeout(() => {

        btn.innerHTML = "📂 Upload PDF";
        btn.disabled = false;

        // Reset file input so the same file can be selected again
        document.getElementById("pdfFile").value = "";

    }, 2000);

}

async function loadRecentDocs(){

    const r = await fetch(API + "/list");

    const docs = await r.json();

    const container = document.getElementById("recentDocs");

    if(docs.length===0){

        container.innerHTML =
        "<p class='empty-docs'>No documents yet</p>";

        return;

    }

    let html="";

    docs.reverse().forEach(doc=>{

        html+=`

        <div class="doc-item">

            🟢 ${doc.title}

        </div>

        `;

    });

    container.innerHTML=html;

}

loadStatus();
drawVectors();
loadRecentDocs();

document
.getElementById("pdfFile")
.addEventListener("change", uploadPDF);

