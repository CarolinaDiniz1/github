function load() {
  chrome.runtime.sendMessage({ type: "GET_SETTINGS" }, s => {
    document.getElementById("likeDelay").value = s.likeDelay || 30;
    document.getElementById("commentDelay").value = s.commentDelay || 60;
    document.getElementById("maxLikesPerHour").value = s.maxLikesPerHour || 50;
    document.getElementById("maxCommentsPerHour").value = s.maxCommentsPerHour || 10;
    document.getElementById("comments").value = (s.comments || []).join("\n");
    document.getElementById("targetHashtags").value = (s.targetHashtags || []).join(", ");
  });
}

document.getElementById("btn-save").addEventListener("click", () => {
  chrome.runtime.sendMessage({ type: "GET_SETTINGS" }, current => {
    const updated = {
      ...current,
      likeDelay: parseInt(document.getElementById("likeDelay").value) || 30,
      commentDelay: parseInt(document.getElementById("commentDelay").value) || 60,
      maxLikesPerHour: parseInt(document.getElementById("maxLikesPerHour").value) || 50,
      maxCommentsPerHour: parseInt(document.getElementById("maxCommentsPerHour").value) || 10,
      comments: document.getElementById("comments").value.split("\n").map(c => c.trim()).filter(Boolean),
      targetHashtags: document.getElementById("targetHashtags").value.split(",").map(h => h.trim()).filter(Boolean)
    };

    chrome.runtime.sendMessage({ type: "SAVE_SETTINGS", data: updated }, () => {
      const msg = document.getElementById("save-msg");
      msg.textContent = "✅ Salvo com sucesso!";
      setTimeout(() => msg.textContent = "", 2500);
    });
  });
});

load();
