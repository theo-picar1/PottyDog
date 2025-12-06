import { Settings, Moon, LogOut, Bell, Droplets } from 'lucide-react'

function PottyTracker() {
    return (
        <div className="min-h-screen flex justify-center items-center">
            {/* Main Content */}
            <div className="max-w-2xl mx-auto px-4 py-8">
                <div className={`bg-blue-900 rounded-3xl p-8 text-white shadow-2xl mb-6`}>
                    <div className="text-center">
                        <div className="flex justify-center">
                            <img 
                                className="w-64"
                                src="/images/happy_dog.png"
                            />
                        </div>
                        <h1 className="text-white mb-2 text-4xl font-bold">Successful Potty</h1>
                        <p className="text-white/90 max-w-md mx-auto">Thank you for letting my out!</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PottyTracker