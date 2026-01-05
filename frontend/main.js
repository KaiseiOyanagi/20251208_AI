document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("categorySelect");
  const button = document.getElementById("loadBtn");
  const list = document.getElementById("newsList");

  button.addEventListener("click", async () => {
    const category = select.value;

    list.innerHTML = "読み込み中...";

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/news?category=${category}`
      );

      if (!response.ok) {
        throw new Error("APIエラー");
      }

      const news = await response.json();
      list.innerHTML = "";

      if (news.length === 0) {
        list.innerHTML = "ニュースが取得できませんでした";
        return;
      }

      news.forEach(item => {
        const div = document.createElement("div");
        div.innerHTML = `
          <h3>${item.title}</h3>
          <p>${item.summary}</p>
          <p><b>タグ:</b> ${item.tags.join(", ")}</p>
          <a href="${item.link}" target="_blank">続きを読む</a>
          <hr>
        `;
        list.appendChild(div);
      });

    } catch (err) {
      console.error(err);
      list.innerHTML = "エラーが発生しました";
    }
  });
});