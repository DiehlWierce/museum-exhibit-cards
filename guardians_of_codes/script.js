// Пункты меню: [папка, название]
const folders = [
  ["guardians_of_codes", "Хранители кодов"],
  ["quadratus", "Квадратус"],
  ["raketus", "Ракетус"]
];

const menu = document.getElementById("menu");

folders.forEach(([folder, displayName]) => {
  const link = document.createElement("a");
  link.href = `${folder}/index.html`;
  link.className = "item";
  link.textContent = displayName;
  menu.appendChild(link);
});
