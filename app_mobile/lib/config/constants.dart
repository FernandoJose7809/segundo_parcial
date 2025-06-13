import 'package:flutter/material.dart';

// ✅ API BASE URL
const String apiBaseUrl =
    'http://10.0.2.2:8000/api/'; // Para pruebas en emulador android

/* const String apiBaseUrl =
    'http://192.168.0.18:8000/api'; */ // para pruebas en celular

/* const String apiBaseUrl = 'http://3.92.188.9:80/api'; */

// ✅ COLORES PRINCIPALES
const Color primaryColor = Color(0xFF3F51B5); // Azul
const Color accentColor = Color(0xFFFFC107); // Amarillo
const Color backgroundColor = Color(0xFFF5F5F5); // Fondo gris claro
const Color errorColor = Colors.redAccent; // Rojo

// ✅ PADDING Y DISEÑO
const double defaultPadding = 16.0;
const double borderRadius = 12.0;
const double buttonPadding = 14.0;

// ✅ ESTILOS DE TEXTO
const TextStyle headerStyle = TextStyle(
  fontSize: 26,
  fontWeight: FontWeight.bold,
  color: Colors.black87,
);

const TextStyle labelStyle = TextStyle(
  fontSize: 16,
  color: Color.fromARGB(136, 0, 0, 0),
);

const TextStyle inputTextStyle = TextStyle(
  fontSize: 16,
);

const TextStyle buttonTextStyle = TextStyle(
  fontSize: 16,
  fontWeight: FontWeight.w600,
  color: Colors.white,
);

const TextStyle smallTextStyle = TextStyle(
  fontSize: 14,
  color: Colors.grey,
);

Color colorEstadoOrden(String estado) {
  switch (estado.toLowerCase()) {
    case 'exitoso':
      return Colors.green;
    case 'pendiente':
      return Colors.orange;
    case 'fallido':
    case 'cancelado':
      return Colors.red;
    default:
      return Colors.grey;
  }
}

final ButtonStyle elevatedButtonStyle = ElevatedButton.styleFrom(
  foregroundColor: Colors.white, backgroundColor: primaryColor, // Texto blanco
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(borderRadius),
  ),
  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
  textStyle: buttonTextStyle,
);

// ✅ INPUT FIELD DECORATION (para que sea consistente en todos los formularios)
final InputDecoration inputDecoration = InputDecoration(
  contentPadding: const EdgeInsets.symmetric(vertical: 20),
  border: OutlineInputBorder(
    borderRadius: BorderRadius.circular(borderRadius),
    borderSide: const BorderSide(color: primaryColor, width: 1),
  ),
  enabledBorder: OutlineInputBorder(
    borderRadius: BorderRadius.circular(borderRadius),
    // ignore: deprecated_member_use
    borderSide: BorderSide(color: primaryColor.withOpacity(0.5), width: 1),
  ),
  focusedBorder: OutlineInputBorder(
    borderRadius: BorderRadius.circular(borderRadius),
    borderSide: const BorderSide(color: primaryColor, width: 2),
  ),
  prefixIcon: const Icon(Icons.person_outline),
);
