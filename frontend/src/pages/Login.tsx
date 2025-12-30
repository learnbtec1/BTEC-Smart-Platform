export default function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-900 dark:to-gray-800">
      <div className="bg-white dark:bg-gray-900 shadow-xl rounded-2xl p-10 w-96 border border-gray-100 dark:border-gray-700">
        <h1 className="text-3xl font-extrabold text-center mb-8 text-gray-800 dark:text-white">
          BTEC Smart Platform
        </h1>

        <div className="flex flex-col gap-5">
          <div className="flex flex-col">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Email
            </label>
            <input
              type="email"
              placeholder="Enter your email"
              className="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition dark:bg-gray-800 dark:border-gray-700 dark:text-white"
            />
          </div>

          <div className="flex flex-col">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Password
            </label>
            <input
              type="password"
              placeholder="Enter your password"
              className="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition dark:bg-gray-800 dark:border-gray-700 dark:text-white"
            />
          </div>

          <button className="bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition font-semibold">
            Login
          </button>
        </div>
      </div>
    </div>
  );
}