const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

window.drawVectors = async function () {
    
    const res = await fetch("/points");
    const points = await res.json();

    console.log(points);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Background
    ctx.fillStyle = "#081122";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Axes
    ctx.strokeStyle = "#2a3555";

    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, canvas.height / 2);
    ctx.lineTo(canvas.width, canvas.height / 2);
    ctx.stroke();

    // Draw points
    points.forEach(point => {

        const x = canvas.width / 2 + point.x;
        const y = canvas.height / 2 - point.y;

        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);

        ctx.fillStyle = "#38bdf8";
        ctx.fill();

        ctx.fillStyle = "white";
        ctx.font = "12px Arial";
        ctx.fillText(point.title, x + 10, y);
    });

}