import json
import os
import requests
import dotenv

# Cargar las variables de entorno desde el archivo .env
dotenv.load_dotenv()


def obtener_clasificaciones_niza_hf(descripcion):
    """
    Analiza la descripción del emprendimiento utilizando modelos de Hugging Face para determinar
    las clasificaciones Niza más apropiadas.

    Args:
        descripcion (str): Descripción detallada del emprendimiento

    Returns:
        dict: Diccionario con las clasificaciones Niza relevantes
    """
    try:
        # Definir las clasificaciones Niza con información detallada
        clasificaciones_info = {
            "1": "Productos químicos destinados a la industria, ciencia, fotografía, agricultura, horticultura y silvicultura; resinas artificiales en bruto, materias plásticas en bruto; abonos para el suelo; composiciones extintoras; preparaciones para templar y soldar metales; productos químicos para conservar alimentos; materias curtientes; adhesivos (pegamentos) destinados a la industria.",
            "2": "Pinturas, barnices, lacas; productos contra la herrumbre y el deterioro de la madera; colorantes, tintes; tintas de imprenta, tintas de marcado y tintas de grabado; resinas naturales en bruto; metales en hojas y en polvo para la pintura, la decoración, la imprenta y trabajos artísticos.",
            "3": "Productos cosméticos y preparaciones de tocador no medicinales; dentífricos no medicinales; productos de perfumería, aceites esenciales; preparaciones para blanquear y otras sustancias para lavar la ropa; preparaciones para limpiar, pulir, desengrasar y raspar.",
            "4": "Aceites y grasas para uso industrial, ceras; lubricantes; composiciones para absorber, rociar y asentar el polvo; combustibles y materiales de alumbrado; velas y mechas de iluminación.",
            "5": "Productos farmacéuticos, preparaciones para uso médico y veterinario; productos higiénicos y sanitarios para uso médico; alimentos y sustancias dietéticas para uso médico o veterinario, alimentos para bebés; suplementos alimenticios para personas o animales; emplastos, material para apósitos; material para empastes e impresiones dentales; desinfectantes; productos para eliminar animales dañinos; fungicidas, herbicidas.",
            "6": "Metales comunes y sus aleaciones, minerales metalíferos; materiales de construcción y edificación metálicos; construcciones transportables metálicas; cables e hilos metálicos no eléctricos; pequeños artículos de ferretería metálicos; recipientes metálicos de almacenamiento y transporte; cajas de caudales.",
            "7": "Máquinas, máquinas herramientas y herramientas mecánicas; motores, excepto motores para vehículos terrestres; acoplamientos y elementos de transmisión, excepto para vehículos terrestres; instrumentos agrícolas que no sean herramientas de mano que funcionan manualmente; incubadoras de huevos; distribuidores automáticos.",
            "8": "Herramientas e instrumentos de mano accionados manualmente; artículos de cuchillería, tenedores y cucharas; armas blancas; maquinillas de afeitar.",
            "9": "Aparatos e instrumentos científicos, náuticos, geodésicos, fotográficos, cinematográficos, ópticos, de pesaje, de medición, de señalización, de control (inspección), de salvamento y de enseñanza; aparatos e instrumentos de conducción, distribución, transformación, acumulación, regulación o control de la electricidad; aparatos de grabación, transmisión o reproducción de sonido o imágenes; soportes de registro magnéticos, discos acústicos; DVDs y otros soportes de grabación digitales; mecanismos para aparatos de previo pago; cajas registradoras, máquinas de calcular, equipos de procesamiento de datos, ordenadores; software; extintores.",
            "10": "Aparatos e instrumentos quirúrgicos, médicos, odontológicos y veterinarios; miembros, ojos y dientes artificiales; artículos ortopédicos; material de sutura; dispositivos terapéuticos y de asistencia para personas con discapacidad; aparatos de masaje; aparatos, dispositivos y artículos de puericultura; aparatos, dispositivos y artículos para actividades sexuales.",
            "11": "Aparatos e instalaciones de alumbrado, calefacción, enfriamiento, producción de vapor, cocción, secado, ventilación y distribución de agua, así como instalaciones sanitarias.",
            "12": "Vehículos; aparatos de locomoción terrestre, aérea o acuática.",
            "13": "Armas de fuego; municiones y proyectiles; explosivos; fuegos artificiales.",
            "14": "Metales preciosos y sus aleaciones; artículos de joyería, piedras preciosas y semipreciosas; artículos de relojería e instrumentos cronométricos.",
            "15": "Instrumentos musicales; atriles para partituras y soportes para instrumentos musicales; batutas.",
            "16": "Papel y cartón; productos de imprenta; material de encuadernación; fotografías; artículos de papelería y artículos de oficina, excepto muebles; adhesivos (pegamentos) de papelería o para uso doméstico; material para artistas y material de dibujo; pinceles; material de instrucción y material didáctico; hojas, películas y bolsas de materias plásticas para embalar y empaquetar; caracteres de imprenta, clichés de imprenta.",
            "17": "Caucho, gutapercha, goma, amianto y mica en bruto o semielaborados, así como sucedáneos de estos materiales; materias plásticas y resinas semielaboradas; materiales para calafatear, estopar y aislar; tubos flexibles no metálicos.",
            "18": "Cuero y cuero de imitación; pieles de animales; artículos de equipaje y bolsas de transporte; paraguas y sombrillas; bastones; fustas, arneses y artículos de guarnicionería; collares, correas y ropa para animales.",
            "19": "Materiales de construcción no metálicos; tubos rígidos no metálicos para la construcción; asfalto, pez, alquitrán y betún; construcciones transportables no metálicas; monumentos no metálicos.",
            "20": "Muebles, espejos, marcos; contenedores no metálicos de almacenamiento o transporte; hueso, cuerno, ballena o nácar, en bruto o semielaborados; conchas; espuma de mar; ámbar amarillo.",
            "21": "Utensilios y recipientes para uso doméstico y culinario; utensilios de cocina y vajilla, excepto tenedores, cuchillos y cucharas; peines y esponjas; cepillos; materiales para fabricar cepillos; material de limpieza; vidrio en bruto o semielaborado, excepto el vidrio de construcción; artículos de cristalería, porcelana y loza.",
            "22": "Cuerdas y cordeles; redes; tiendas de campaña y lonas; toldos de materias textiles o sintéticas; velas de navegación; sacos para el transporte y almacenamiento de mercancías a granel; materiales de acolchado y relleno, excepto el papel, cartón, caucho o materias plásticas; materias textiles fibrosas en bruto y sus sucedáneos.",
            "23": "Hilos para uso textil.",
            "24": "Tejidos y sus sucedáneos; ropa de hogar; cortinas de materias textiles o de materias plásticas.",
            "25": "Prendas de vestir, calzado, artículos de sombrerería.",
            "26": "Encajes, cordones y bordados, así como cintas y lazos de mercería; botones, ganchos y ojetes, alfileres y agujas; flores artificiales; adornos para el cabello; cabello postizo.",
            "27": "Alfombras, felpudos, esteras, linóleo y otros revestimientos de suelos; tapices murales que no sean de materias textiles.",
            "28": "Juegos y juguetes; aparatos de videojuegos; artículos de gimnasia y deporte; adornos para árboles de Navidad.",
            "29": "Carne, pescado, carne de ave y carne de caza; extractos de carne; frutas y verduras, hortalizas y legumbres en conserva, congeladas, secas y cocidas; jaleas, confituras, compotas; huevos; leche, quesos, mantequilla, yogur y otros productos lácteos; aceites y grasas para uso alimenticio.",
            "30": "Café, té, cacao y sucedáneos del café; arroz, pastas alimenticias y fideos; tapioca y sagú; harinas y preparaciones a base de cereales; pan, productos de pastelería y confitería; chocolate; helados cremosos, sorbetes y otros helados; azúcar, miel, jarabe de melaza; levadura, polvos de hornear; sal, productos para sazonar, especias, hierbas en conserva; vinagre, salsas y otros condimentos; hielo.",
            "31": "Productos agrícolas, acuícolas, hortícolas y forestales en bruto y sin procesar; granos y semillas en bruto o sin procesar; frutas y verduras, hortalizas y legumbres frescas, hierbas aromáticas frescas; plantas y flores naturales; bulbos, plantones y semillas para plantar; animales vivos; productos alimenticios y bebidas para animales; malta.",
            "32": "Cervezas; bebidas sin alcohol; aguas minerales y gaseosas; bebidas a base de frutas y zumos de frutas; siropes y otras preparaciones sin alcohol para elaborar bebidas.",
            "33": "Bebidas alcohólicas, excepto cervezas; preparaciones alcohólicas para elaborar bebidas.",
            "34": "Tabaco y sucedáneos del tabaco; cigarrillos y puros; cigarrillos electrónicos y vaporizadores bucales para fumadores; artículos para fumadores; cerillas.",
            "35": "Publicidad; gestión, organización y administración de negocios comerciales; trabajos de oficina.",
            "36": "Servicios financieros, monetarios y bancarios; servicios de seguros; negocios inmobiliarios.",
            "37": "Servicios de construcción; servicios de instalación y reparación; extracción minera, perforación de gas y de petróleo.",
            "38": "Servicios de telecomunicaciones.",
            "39": "Transporte; embalaje y almacenamiento de mercancías; organización de viajes.",
            "40": "Tratamiento de materiales; reciclaje de residuos y desechos; purificación del aire y tratamiento del agua; servicios de impresión; conservación de alimentos y bebidas.",
            "41": "Educación; formación; servicios de entretenimiento; actividades deportivas y culturales.",
            "42": "Servicios científicos y tecnológicos, así como servicios de investigación y diseño conexos; servicios de análisis industrial, investigación industrial y diseño industrial; control de calidad y servicios de autenticación; diseño y desarrollo de hardware y software.",
            "43": "Servicios de restauración (alimentación); hospedaje temporal.",
            "44": "Servicios médicos; servicios veterinarios; tratamientos de higiene y de belleza para personas o animales; servicios de agricultura, acuicultura, horticultura y silvicultura.",
            "45": "Servicios jurídicos; servicios de seguridad para la protección física de bienes materiales y personas; servicios personales y sociales prestados por terceros para satisfacer necesidades individuales."
        }

        # Preparar prompt para clasificación
        prompt = f"""Analiza la siguiente descripción de un emprendimiento y determina las 3 clasificaciones Niza más relevantes.
        
Descripción del emprendimiento:
{descripcion}

Las clasificaciones Niza son:
{json.dumps(clasificaciones_info, indent=2)}

Devuelve solo un JSON con el siguiente formato exacto sin incluir texto adicional, ni siquiera saltos de línea ('\ n'), todo en un mismo renglón:
{{
  "clasificaciones": [
    {{
      "clase": "NÚMERO_DE_CLASE",
      "descripcion": "DESCRIPCIÓN_OFICIAL_DE_LA_CLASE",
      "relevancia": "EXPLICACIÓN_DE_POR_QUÉ_ES_RELEVANTE",
      "confianza": PORCENTAJE_DE_CONFIANZA_ENTRE_0_Y_100
    }},
    ...
  ]
}}
"""

        # URL de la API de Hugging Face Inference - Usamos Mixtral, un modelo más potente
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"

        # Cabeceras para la API
        hf_api_key = os.environ.get("HUGGINGFACE_API_KEY")
        headers = {"Authorization": f"Bearer {hf_api_key}"}

        # Datos para la solicitud
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1024,
                "temperature": 0.3,
                "top_p": 0.9,
                "return_full_text": False
            }
        }

        # Realizar solicitud y mostrar información de depuración
        print(f"Realizando solicitud a Hugging Face API: {API_URL}")
        if hf_api_key:
            print(f"Usando token de acceso: {hf_api_key[:5]}...")
        else:
            print("ADVERTENCIA: No se ha proporcionado token de acceso para Hugging Face")

        response = requests.post(API_URL, headers=headers, json=payload)

        # Imprimir respuesta para depuración
        print(
            f"Respuesta de Hugging Face - Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        print(f"Headers: {response.headers}")

        # Verificar si hubo error en la solicitud
        if response.status_code != 200:
            print(f"Error en respuesta de Hugging Face: {response.text}")
            return {
                "clasificaciones": [
                    {
                        "clase": "Error: Servicio de Hugging Face no disponible",
                        "descripcion": f"No se pudo conectar con el servicio de Hugging Face. Código de error: {response.status_code}",
                        "relevancia": "Por favor, intenta nuevamente más tarde o utiliza el modo de demostración.",
                        "confianza": 0
                    }
                ]
            }

        try:
            # Extraer el texto generado
            response_data = response.json()
            
            # Volver a cargar el JSON de la respuesta
            response_data = json.loads(response_data)
            
            # Si la respuesta no es un JSON válido, intentar convertirla
            # a un JSON válido
            # Si la respuesta es un string, intentar convertirlo a JSON
            if isinstance(response_data, str):
                try:
                    response_data = json.loads(response_data)
                except json.JSONDecodeError:
                    # Si no se puede convertir, usar el texto original
                    response_data = response_data

            # Manejar diferentes formatos de respuesta de HF
            if isinstance(response_data, list) and len(response_data) > 0:
                if "generated_text" in response_data[0]:
                    generated_text = response_data[0]["generated_text"]
                else:
                    # Otro formato posible
                    generated_text = str(response_data)
            else:
                generated_text = str(response_data)

            # Buscar el JSON en el texto generado
            # Primera estrategia: buscar el patrón json completo
            start_idx = generated_text.find("{")
            end_idx = generated_text.rfind("}") + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_result = generated_text[start_idx:end_idx]
                try:
                    result = json.loads(json_result)

                    # Formatear el resultado para asegurar estructura correcta
                    formatted_result = {"clasificaciones": []}

                    if "clasificaciones" in result:
                        for item in result.get("clasificaciones", [])[:3]:
                            formatted_item = {
                                "clase": str(item.get("clase", "")),
                                "descripcion": str(item.get("descripcion", "")),
                                "relevancia": str(item.get("relevancia", "")),
                                "confianza": int(item.get("confianza", 0))
                            }
                            formatted_result["clasificaciones"].append(
                                formatted_item)

                        if formatted_result["clasificaciones"]:
                            return formatted_result
                except json.JSONDecodeError:
                    # Continuar con el siguiente enfoque
                    pass

            # Si no pudimos extraer un JSON válido, crear una respuesta manualmente
            # basada en el texto generado

            # Evaluar si el texto menciona algunas clases Niza
            clases_encontradas = []
            for i in range(1, 46):  # Clases Niza van del 1 al 45
                if f"Clase {i}" in generated_text or f"clase {i}" in generated_text or f"CLASE {i}" in generated_text:
                    clases_encontradas.append(str(i))

            # Si encontramos al menos una clase, crear un resultado artificial
            if clases_encontradas:
                formatted_result = {"clasificaciones": []}
                for i, clase in enumerate(clases_encontradas[:3]):
                    # Primera clase 90%, segunda 80%, tercera 70%
                    confianza = 90 - (i * 10)
                    info_clase = clasificaciones_info.get(clase, "")
                    formatted_item = {
                        "clase": clase,
                        "descripcion": info_clase,
                        "relevancia": f"Esta clase parece relevante para tu emprendimiento según el análisis del texto.",
                        "confianza": confianza
                    }
                    formatted_result["clasificaciones"].append(formatted_item)

                if formatted_result["clasificaciones"]:
                    return formatted_result

            # Si no se pudo extraer información útil
            return {
                "clasificaciones": [
                    {
                        "clase": "Error: Formato inválido",
                        "descripcion": "No se pudo interpretar correctamente la respuesta del modelo.",
                        "relevancia": "Por favor, intenta nuevamente o usa el modo de demostración.",
                        "confianza": 0
                    }
                ]
            }
        except Exception as e:
            # Cualquier otro error en el procesamiento
            print(f"Error al procesar respuesta de Hugging Face: {str(e)}")
            return {
                "clasificaciones": [
                    {
                        "clase": "Error: Formato inválido",
                        "descripcion": "Error al procesar la respuesta del modelo: " + str(e),
                        "relevancia": "Por favor, intenta nuevamente o usa el modo de demostración.",
                        "confianza": 0
                    }
                ]
            }

    except Exception as e:
        # En caso de cualquier otro error
        return {
            "clasificaciones": [
                {
                    "clase": "Error: Servicio no disponible",
                    "descripcion": f"Error al procesar la solicitud: {str(e)}",
                    "relevancia": "Por favor, intenta nuevamente más tarde o utiliza el modo de demostración.",
                    "confianza": 0
                }
            ]
        }
