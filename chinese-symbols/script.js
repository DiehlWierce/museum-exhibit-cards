// Пункты меню: [папка, название]
const folders = [
  ["child", "Ребенок"],
  ["family", "Семья"],
  ["happiness", "Счастье"],
  ["love", "Любовь"],
  ["sun", "Солнце"]
];

const menu = document.getElementById("menu");

folders.forEach(([folder, displayName]) => {
  const link = document.createElement("a");
  link.href = `${folder}/index.html`;
  link.className = "item";
  link.textContent = displayName;
  menu.appendChild(link);
});
