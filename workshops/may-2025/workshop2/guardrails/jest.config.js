module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  // Explicitly specify to run tests from src directory only
  roots: ['<rootDir>/src'],
  // Specify test file patterns more precisely
  testMatch: [
    '**/__tests__/**/*.test.ts',
    '**/?(*.)+(spec|test).ts'
  ],
  // Explicitly exclude declaration files and the dist directory
  testPathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '\\.d\\.ts$'
  ],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  moduleNameMapper: {
    '^src/(.*)$': '<rootDir>/src/$1'
  },
  transform: {
    '^.+\\.tsx?$': [
      'ts-jest',
      {
        tsconfig: 'tsconfig.json'
      }
    ]
  },
  // Force Jest to exit after all tests complete
  forceExit: true,
  // Set a longer timeout for tests that interact with external APIs
  testTimeout: 15000
};