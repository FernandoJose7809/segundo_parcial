import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:app_mobile/config/constants.dart';

class ApiService {
  static const String apiUrl = apiBaseUrl;

  Future<http.Response> get(String endpoint,
      {Map<String, String>? headers}) async {
    final url = Uri.parse(apiUrl + endpoint);
    final response = await http.get(url, headers: headers);
    if (response.statusCode == 401) {
      // Intentar refrescar el token
      final newAccess = await _refreshToken();
      if (newAccess != null && headers != null) {
        headers['Authorization'] = 'Bearer $newAccess';
        return await http.get(url, headers: headers);
      }
    }
    return response;
  }

  Future<http.Response> post(String endpoint, Map<String, dynamic> data,
      {Map<String, String>? headers}) async {
    final url = Uri.parse(apiUrl + endpoint);
    final defaultHeaders = {
      'Content-Type': 'application/json',
      if (headers != null) ...headers,
    };
    return await http.post(
      url,
      headers: defaultHeaders,
      body: jsonEncode(data),
    );
  }

  Future<String?> _refreshToken() async {
    final prefs = await SharedPreferences.getInstance();
    final refresh = prefs.getString('refresh');
    if (refresh == null) return null;

    final url = Uri.parse('${apiUrl}token/refresh/');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'refresh': refresh}),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final newAccess = data['access'];
      await prefs.setString('access', newAccess);
      return newAccess;
    }
    return null;
  }
}
