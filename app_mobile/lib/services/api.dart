import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:app_mobile/config/constants.dart'; // Importa la constante

class ApiService {
  static const String apiUrl = apiBaseUrl; // Usa la constante importada

  Future<http.Response> get(String endpoint) async {
    final url = Uri.parse(apiUrl + endpoint);
    return await http.get(url);
  }

  Future<http.Response> post(String endpoint, Map<String, dynamic> data) async {
    final url = Uri.parse(apiUrl + endpoint);
    return await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(data),
    );
  }

  Future<http.Response> put(String endpoint, Map<String, dynamic> data) async {
    final url = Uri.parse(apiUrl + endpoint);
    return await http.put(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(data),
    );
  }

  Future<http.Response> delete(String endpoint) async {
    final url = Uri.parse(apiUrl + endpoint);
    return await http.delete(url);
  }
}
