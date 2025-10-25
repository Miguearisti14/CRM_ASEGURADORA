// static/js/messages.js

document.addEventListener("DOMContentLoaded", () => {
    // Cerrar mensajes manualmente
    const closeButtons = document.querySelectorAll(".close-message");
    closeButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const msg = btn.closest(".message");
            msg.style.opacity = "0";
            msg.style.transform = "translateX(50px)";
            setTimeout(() => msg.remove(), 300);
        });
    });

    // Auto-desaparición después de 4 segundos
    const messages = document.querySelectorAll(".message");
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = "0";
            msg.style.transform = "translateX(50px)";
            setTimeout(() => msg.remove(), 300);
        }, 4000);
    });
});
