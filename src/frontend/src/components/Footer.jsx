import {
    FaGithub,
    FaLinkedin,
    FaEnvelope,
    FaTwitter,
    FaInstagram,
    FaFacebookF,
    FaStore
} from "react-icons/fa";


export default function Footer() {
    return (
        <footer>
            <div className="container footer-container">
                <div className="footer-column">
                    <img src={`${import.meta.env.BASE_URL}img/icon_small_without_background.png`} alt="icono" />
                </div>


                <div className="footer-column">
                    <h5>Clasificación Niza</h5>
                    <ul>
                        <li><a href="https://www.oepm.es/es/herramientas/buscador-base-de-datos/clasificaciones-internacionales/clasificacion-internacional-de-productos-y-servicios-para-el-registro-de-las-marcas-clasificacion-de-Niza/">¿Qué es?</a></li>
                        <li><a href="https://nclpub.wipo.int/esen/pdf-download.pdf?lang=es&tab=class_headings&dateInForce=20240101">Manual oficial</a></li>
                        <li><a href="https://nclpub.wipo.int/enfr/">Base de datos</a></li>
                    </ul>
                </div>
                <div className="footer-column">
                    <h5>Desarrollador</h5>
                    <h5>David Cajiao</h5>
                    <ul>
                        <li><a href="https://github.com/DCajiao"><FaGithub /> GitHub</a></li>
                        <li><a href="https://www.linkedin.com/in/dcajiao/"><FaLinkedin /> LinkedIn</a></li>
                        <li><a href="mailto:dcajiao@gmail.com"><FaEnvelope /> Gmail</a></li>
                    </ul>
                    <br />
                </div>
                <div className="footer-column">
                    <h5>Analista</h5>
                    <h5>Juan Pablo Granados</h5>
                    <ul>
                        <li><a href="https://github.com/JhinPablo"><FaGithub /> GitHub</a></li>
                        <li><a href="https://www.linkedin.com/in/juan-pablo-g-125275219/"><FaLinkedin /> LinkedIn</a></li>
                        <li><a href="#"><FaEnvelope /> Gmail</a></li>
                    </ul>
                </div>
                <div className="footer-column">
                    <h5>Asesoría Legal</h5>
                    <h5>Jorge Alberto Villegas</h5>
                    <ul>
                        <li><a href="#"><FaStore /> UAO</a></li>
                        <li><a href="https://www.linkedin.com/in/jorge-alberto-villegas-restrepo-9893341a4/?originalSubdomain=co"><FaLinkedin /> LinkedIn</a></li>
                        <li><a href="#"><FaEnvelope /> Contacto</a></li>
                    </ul>
                </div>
            </div>
            <div className="footer-bottom">
                © {new Date().getFullYear()} Clasificador Niza — Todos los derechos reservados.
            </div>
        </footer>

    );
}