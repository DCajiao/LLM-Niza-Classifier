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
                    <img src="../../public/img/icon_small_without_background.png" alt="" />
                </div>


                <div className="footer-column">
                    <h5>Clasificación Niza</h5>
                    <ul>
                        <li><a href="#">¿Qué es?</a></li>
                        <li><a href="#">Manual oficial</a></li>
                        <li><a href="#">Base de datos</a></li>
                    </ul>
                </div>
                <div className="footer-column">
                    <h5>Desarrollador</h5>
                    <h5>David</h5>
                    <ul>
                        <li><a href="#"><FaGithub /> GitHub</a></li>
                        <li><a href="#"><FaLinkedin /> LinkedIn</a></li>
                        <li><a href="#"><FaEnvelope /> developer@example.com</a></li>
                    </ul>
                    <br />
                </div>
                <div className="footer-column">
                    <h5>Analista</h5>
                    <h5>Juan Pa</h5>
                    <ul>
                        <li><a href="#"><FaGithub /> GitHub</a></li>
                        <li><a href="#"><FaLinkedin /> LinkedIn</a></li>
                        <li><a href="#"><FaEnvelope /> developer@example.com</a></li>
                    </ul>
                </div>
                <div className="footer-column">
                    <h5>Asesoría Legal</h5>
                    <h5>Jorge Villegas</h5>
                    <ul>
                        <li><a href="#"><FaStore /> UAO</a></li>
                        <li><a href="#"><FaLinkedin /> LinkedIn</a></li>
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