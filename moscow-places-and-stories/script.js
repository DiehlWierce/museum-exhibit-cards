// Пункты меню: [папка, название]
const folders = [
  ["ded-moroz-estate", "Московская усадьба Деда Мороза"],
  ["friendship-of-peoples-fountain", "Фонтан «Дружба народов»"],
  ["luzhniki-sports-complex", "Спорткомплекс «Лужники»"],
  ["mtsk-belokamennaya", "МЦК «Белокаменная»"],
  ["mtsk-panfilovskaya", "МЦК «Панфиловская»"],
  ["novoarbatskiy-most", "Новоарбатский мост"],
  ["poklonnaya-gora-park-pobedy", "Поклонная гора и Парк Победы"],
  ["sokolniki-amusement-park", "Парк аттракционов «Сокольники»"],
  ["sokolniki-fire-tower", "Пожарная каланча в Сокольниках"],
  ["southern-river-port", "Южный речной порт"],
  ["state-kremlin-palace", "Государственный Кремлёвский дворец"],
  ["tretyakov-gallery", "Третьяковская галерея"]
];

const menu = document.getElementById("menu");

folders.forEach(([folder, displayName]) => {
  const link = document.createElement("a");
  link.href = `${folder}/index.html`;
  link.className = "item";
  link.textContent = displayName;
  menu.appendChild(link);
});
