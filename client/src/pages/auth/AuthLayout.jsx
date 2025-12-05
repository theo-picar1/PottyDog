function AuthLayout({ children, title, message }) {
    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-[#F2F6FF] p-12">
            <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8">
                <h1 className="text-2xl font-bold text-center mb-2 text-gray-900">
                    {title}
                </h1>

                <p className="text-center mb-6 text-gray-600 text-sm">
                    {message}
                </p>
                
                <div className="space-y-4">
                    {children}
                </div>
            </div>
        </div>
    )
}

export default AuthLayout