import AuthLayout from "./AuthLayout"
import { Lock, Mail } from 'lucide-react'

function Login() {
    return (
        <AuthLayout>
            {/* Login Form */}
            <form className="space-y-4">
                <div>
                    <label htmlFor="email" className="block text-gray-700 mb-2">
                        Email
                    </label>
                    <div className="relative">
                        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <input
                            id="email"
                            type="email"
                            className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="your@email.com"
                            required
                        />
                    </div>
                </div>

                <div>
                    <label htmlFor="password" className="block text-gray-700 mb-2">
                        Password
                    </label>
                    <div className="relative">
                        <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <input
                            id="password"
                            type="password"
                            className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="••••••••"
                            required
                        />
                    </div>
                </div>

                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-3 rounded-xl hover:bg-blue-600 transition-all duration-200 shadow-lg hover:shadow-xl"
                >
                    Sign In
                </button>
            </form>

            {/* Register Link */}
            <div className="mt-6 text-center">
                <p className="text-gray-600">
                    Don't have an account?{' '}
                    <button className="text-blue-600 hover:text-blue-700">
                        Sign up
                    </button>
                </p>
            </div>
        </AuthLayout>
    )
}

export default Login