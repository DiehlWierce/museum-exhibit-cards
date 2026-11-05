// Карточки раздела: [папка, название]
const folders = [
  ["state-kremlin-palace", "Государственный Кремлёвский дворец"],
  ["mtsk-belokamennaya", "МЦК «Белокаменная»"],
  ["mtsk-panfilovskaya", "МЦК «Панфиловская»"],
  ["novoarbatskiy-most", "Новоарбатский мост"],
  ["sokolniki-amusement-park", "Парк аттракционов «Сокольники»"],
  ["sokolniki-fire-tower", "Пожарная каланча в Сокольниках"],
  ["poklonnaya-gora-park-pobedy", "Поклонная гора и Парк Победы"],
  ["luzhniki-sports-complex", "Спорткомплекс «Лужники»"],
  ["tretyakov-gallery", "Третьяковская галерея"],
  ["ded-moroz-estate", "Московская усадьба Деда Мороза"],
  ["friendship-of-peoples-fountain", "Фонтан «Дружба народов»"],
  ["southern-river-port", "Южный речной порт"],
];

const menu = document.getElementById("menu");

folders.forEach(([folder, displayName]) => {
  const link = document.createElement("a");
  link.href = `${folder}/index.html`;
  link.className = "item";
  link.textContent = displayName;
  menu.appendChild(link);
});
