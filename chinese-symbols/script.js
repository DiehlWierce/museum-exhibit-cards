// Массив папок: [имя папки на диске, отображаемое имя на русском]
const folders = [
  ["child", "Ребенок"],
  ["family", "Семья"],
  ["happiness", "Счастье"],
  ["love", "Любовь"],
  ["sun", "Солнце"],
];

const menu = document.getElementById("menu");

folders.forEach(([folder, displayName]) => {
  const link = document.createElement("a");
  link.href = `${folder}/index.html`;  // путь совпадает с именем папки
  link.className = "item";
  link.textContent = displayName;      // отображаем красивое имя
  menu.appendChild(link);
});