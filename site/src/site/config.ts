export type Lang = 'ca' | 'es';
export const LANGS: Lang[] = ['ca', 'es'];
export const CODI_IDIOMA: Record<Lang, string> = { ca: 'ca', es: 'es' };
export const BASE = '/franciscaineditos';

export const SITE = {
  nom: { ca: 'Escrits inèdits', es: 'Escritos inéditos' },
  autora: 'Francisca Julián Querol',
  lema: {
    ca: 'Els textos de Francisca Julián Querol que no havien eixit mai de l’ordinador, triats un a un',
    es: 'Los textos de Francisca Julián Querol que nunca habían salido del ordenador, elegidos uno a uno',
  },
  repositori: 'https://github.com/jtpadilla/franciscaineditos',
};

/** Les obres, per la clau que és el nom de la carpeta de md/ passat a slug, en l'ordre en què es presenten. */
export const OBRES: Record<string, { nom: Record<Lang, string>; desc: Record<Lang, string> }> = {
  'memoria-familiar': {
    nom: { ca: 'Memòria familiar', es: 'Memoria familiar' },
    desc: { ca: 'El llibre de memòries de 2026 i «Qui ho farà?», la versió de 2014 amb les seues fotos; la genealogia dels Julián Segura i dels Boix; fotos antigues i records de Cinctorres en primera persona.',
            es: 'El libro de memorias de 2026 y «Qui ho farà?», la versión de 2014 con sus fotos; la genealogía de los Julián Segura y los Boix; fotos antiguas y recuerdos de Cinctorres en primera persona.' } },
  'mon-rural-i-cuina': {
    nom: { ca: 'Món rural i cuina', es: 'Mundo rural y cocina' },
    desc: { ca: 'El gran treball sobre l’agricultura i els costums del camp de Castelló, la tòfona negra, la pedra en sec, els oficis, les masies, els jocs de xiquets i les receptes de casa.',
            es: 'El gran trabajo sobre la agricultura y las costumbres del campo de Castellón, la trufa negra, la piedra en seco, los oficios, las masías, los juegos de niños y las recetas de casa.' } },
  cinctorres: {
    nom: { ca: 'Cinctorres', es: 'Cinctorres' },
    desc: { ca: 'El poble: la carta pobla, l’església, les ermites i les rogatives, el Pont Vell, els teixidors i els faixeros, la festa del foc i Sant Antoni.',
            es: 'El pueblo: la carta puebla, la iglesia, las ermitas y las rogativas, el Pont Vell, los tejedores y los faixeros, la fiesta del fuego y Sant Antoni.' } },
  castello: {
    nom: { ca: 'Castelló', es: 'Castellón' },
    desc: { ca: 'La ciutat on va viure: els carrers antics, el mercat de Sant Antoni i el del dilluns, les fires, el quarter de Sant Francesc, la toponímia de les partides, el paviment ceràmic.',
            es: 'La ciudad donde vivió: las calles antiguas, el mercado de San Antonio y el del lunes, las ferias, el cuartel de San Francisco, la toponimia de las partidas, el pavimento cerámico.' } },
  listo: {
    nom: { ca: 'Listo', es: 'Listo' },
    desc: { ca: 'Les entrades del blog narrades pel seu gos, Listo, tal com les va polir per al llibre «Em diuen Listo», i el comiat que li va escriure.',
            es: 'Las entradas del blog narradas por su perro, Listo, tal como las pulió para el libro «Em diuen Listo», y la despedida que le escribió.' } },
  'treballs-i-reflexions': {
    nom: { ca: 'Treballs i reflexions', es: 'Trabajos y reflexiones' },
    desc: { ca: 'Treballs de curs, ressenyes, conferències i textos d’opinió: la bellesa, la felicitat, el Quixot, el Sexenni, la Balma, les noves tecnologies.',
            es: 'Trabajos de curso, reseñas, conferencias y textos de opinión: la belleza, la felicidad, el Quijote, el Sexenni, la Balma, las nuevas tecnologías.' } },
  'poemes-i-reflexions': {
    nom: { ca: 'Poemes i reflexions', es: 'Poemas y reflexiones' },
    desc: { ca: 'Poemes i textos breus en vers o en prosa curta: la pedra, les flors, els cinc sentits, el Mediterrani.',
            es: 'Poemas y textos breves en verso o en prosa corta: la piedra, las flores, los cinco sentidos, el Mediterráneo.' } },
  religion: {
    nom: { ca: 'Religió', es: 'Religión' },
    desc: { ca: 'Els treballs del curs de religió medieval de la Universitat per a Majors (2016-2017): croades, ordes militars, monacat, Inquisició, Maimònides, Ramon Llull.',
            es: 'Los trabajos del curso de religión medieval de la Universitat per a Majors (2016-2017): cruzadas, órdenes militares, monacato, Inquisición, Maimónides, Ramon Llull.' } },
  natura: {
    nom: { ca: 'Natura', es: 'Naturaleza' },
    desc: { ca: 'El treball de biodiversitat de la Rambla Celumbres, amb les seues 111 fotos, els articles del butlletí de Cinctorres i les estacions.',
            es: 'El trabajo de biodiversidad de la Rambla Celumbres, con sus 111 fotos, los artículos del boletín de Cinctorres y las estaciones.' } },
  relats: {
    nom: { ca: 'Relats', es: 'Relatos' },
    desc: { ca: 'Contes i relats: un conte de nuvis, un viatge, la Maragateria, una nit de tempesta.',
            es: 'Cuentos y relatos: un cuento de novios, un viaje, la Maragatería, una noche de tormenta.' } },
  'familia-padilla-agut': {
    nom: { ca: 'Família Padilla Agut', es: 'Familia Padilla Agut' },
    desc: { ca: 'La família del seu marit, Juan Padilla Agut: l’àvia Maria, la cançó de l’agüelo Padilla, el poble de Padilla.',
            es: 'La familia de su marido, Juan Padilla Agut: la abuela María, la canción del agüelo Padilla, el pueblo de Padilla.' } },
  'polo-de-bernabe': {
    nom: { ca: 'Polo de Bernabé', es: 'Polo de Bernabé' },
    desc: { ca: 'La recerca genealògica sobre la família Polo de Bernabé de Cinctorres i la transcripció de les seues escriptures d’inventari (1772-1775).',
            es: 'La investigación genealógica sobre la familia Polo de Bernabé de Cinctorres y la transcripción de sus escrituras de inventario (1772-1775).' } },
};

export const T = {
  obres: { ca: 'Obres', es: 'Obras' },
  fotografies: { ca: 'Fotografies', es: 'Fotografías' },
  cerca: { ca: 'Cerca', es: 'Buscar' },
  sobre: { ca: 'Sobre este fons', es: 'Sobre este fondo' },
  autora: { ca: 'L’autora', es: 'La autora' },
  autoraCompleta: { ca: 'Biografia completa i tots els llocs', es: 'Biografía completa y todos los sitios' },
  textos: { ca: 'textos', es: 'textos' },
  text: { ca: 'text', es: 'texto' },
  imatges: { ca: 'imatges', es: 'imágenes' },
  caracters: { ca: 'caràcters', es: 'caracteres' },
  llengua: { ca: 'Llengua', es: 'Lengua' },
  llengues: { ca: { ca: 'valencià', es: 'castellà', mixt: 'valencià i castellà' }, es: { ca: 'valenciano', es: 'castellano', mixt: 'valenciano y castellano' } },
  inferit: { ca: 'deduïda del text', es: 'deducida del texto' },
  notes: { ca: 'Nota de l’edició', es: 'Nota de la edición' },
  tornar: { ca: 'Totes les obres', es: 'Todas las obras' },
  altresLlocs: { ca: 'Els altres llocs de l’autora', es: 'Los otros sitios de la autora' },
  idiomaAlt: { ca: 'Castellano', es: 'Valencià' },
  tema: { ca: 'Tema clar o fosc', es: 'Tema claro u oscuro' },
  anterior: { ca: 'Anterior', es: 'Anterior' },
  seguent: { ca: 'Següent', es: 'Siguiente' },
  peu: { ca: 'Textos i fotografies © Francisca Julián Querol. Els textos es publiquen tal com ella els va escriure, sense corregir-los.',
         es: 'Textos y fotografías © Francisca Julián Querol. Los textos se publican tal como ella los escribió, sin corregirlos.' },
  repositori: { ca: 'Repositori', es: 'Repositorio' },
};

export const GERMANS = [
  { nom: 'Francisca Julián Querol', url: 'https://franciscajulianquerol.es/', desc: { ca: 'l’índex de tots els llocs', es: 'el índice de todos los sitios' } },
  { nom: 'Les meues coses', url: 'https://jtpadilla.github.io/lesmeuescoses/', desc: { ca: 'el blog, 2010–2026', es: 'el blog, 2010–2026' } },
  { nom: 'Masos de Morella', url: 'https://jtpadilla.github.io/masosdemorella/', desc: { ca: 'el llibre dels Llivis', es: 'el libro dels Llivis' } },
  { nom: 'Rambla Celumbres', url: 'https://ramblacelumbres.org/', desc: { ca: 'la biodiversitat de la rambla', es: 'la biodiversidad de la rambla' } },
  { nom: 'Sant Joans', url: 'https://jtpadilla.github.io/santjoans/', desc: { ca: 'el paviment ceràmic de la casa', es: 'el pavimento cerámico de la casa' } },
];

export const url = (lang: Lang, ruta = '') => `${BASE}/${lang === 'es' ? 'es/' : ''}${ruta ? ruta.replace(/^\/|\/$/g, '') + '/' : ''}`;
