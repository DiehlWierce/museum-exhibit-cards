// Пункты меню: [папка, название]
const folders = [
  ["chinese-symbols", "Китайские иероглифы"],
  ["sights-of-moscow", "Достопримечательности Москвы"],
  ["traditional-russian-objects", "Народные предметы"],
  ["guardians_of_codes", "Хранители кодов"],
  ["moscow-places-and-stories", "Москва: места и истории"]
];

const menu = document.getElementById("menu");

folders.forEach(([folder, displayName]) => {
  const link = document.createElement("a");
  link.href = `${folder}/index.html`;
  link.className = "item";
  link.textContent = displayName;
  menu.appendChild(link);
});
