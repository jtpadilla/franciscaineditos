-- Quita ancho/alto y demás atributos de las imágenes para que pandoc las
-- escriba como ![](ruta) en vez de como <img ...> en HTML.
function Image(el)
  el.attributes = {}
  el.classes = {}
  el.identifier = ""
  return el
end
