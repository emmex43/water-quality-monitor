// API Service for Authentication
class AuthAPI {
    static baseURL = '/api/auth';

    static async register(userData) {
        try {
            const response = await fetch(`${this.baseURL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    static async login(credentials) {
        try {
            const response = await fetch(`${this.baseURL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials)
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }

    static async logout() {
        try {
            const response = await fetch(`${this.baseURL}/logout`, {
                method: 'POST',
                credentials: 'include'
            });
            
            const data = await response.json();
            return { success: response.ok, data };
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }
}