class NetworkService {
    static func fetchNumber(completion: @escaping (Result<Int, Error>) -> Void) {
        guard let url = URL(string: "your_server_api_endpoint") else {
            completion(.failure(NSError(domain: "Invalid URL", code: -1, userInfo: nil)))
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "No data received", code: -1, userInfo: nil)))
                return
            }

            do {
                let number = try JSONDecoder().decode(Int.self, from: data)
                completion(.success(number))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
}
