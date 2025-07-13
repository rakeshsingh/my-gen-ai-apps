#!/bin/bash

# Ollama Installation and Model Setup Script
# This script downloads Ollama and installs Llama 3.2 and DeepSeek-R1 models

set -e  # Exit on any error

echo "🚀 Starting Ollama installation and model setup..."
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on supported OS
check_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    print_status "Detected OS: $OS"
}

# Check if Ollama is already installed
check_ollama() {
    if command -v ollama &> /dev/null; then
        print_warning "Ollama is already installed at: $(which ollama)"
        echo -n "Do you want to reinstall? (y/N): "
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            print_status "Skipping Ollama installation"
            return 1
        fi
    fi
    return 0
}

# Install Ollama
install_ollama() {
    print_status "Installing Ollama..."
    
    if [[ "$OS" == "linux" ]]; then
        # Linux installation
        curl -fsSL https://ollama.com/install.sh | sh
    elif [[ "$OS" == "macos" ]]; then
        # macOS installation
        if command -v brew &> /dev/null; then
            print_status "Using Homebrew to install Ollama..."
            brew install ollama
        else
            print_status "Installing Ollama directly..."
            curl -fsSL https://ollama.com/install.sh | sh
        fi
    fi
    
    print_status "Ollama installation completed!"
}

# Start Ollama service
start_ollama() {
    print_status "Starting Ollama service..."
    
    if [[ "$OS" == "linux" ]]; then
        # Try to start as systemd service first
        if systemctl is-enabled ollama &> /dev/null; then
            sudo systemctl start ollama
            sudo systemctl enable ollama
            print_status "Ollama service started and enabled"
        else
            # Start in background
            nohup ollama serve > /dev/null 2>&1 &
            print_status "Ollama server started in background"
        fi
    elif [[ "$OS" == "macos" ]]; then
        # Start Ollama in background
        nohup ollama serve > /dev/null 2>&1 &
        print_status "Ollama server started in background"
    fi
    
    # Wait for service to be ready
    print_status "Waiting for Ollama service to be ready..."
    sleep 5
    
    # Test if service is running
    if ! ollama list &> /dev/null; then
        print_error "Ollama service failed to start properly"
        exit 1
    fi
    
    print_status "Ollama service is ready!"
}

# Install models
install_models() {
    print_status "Installing AI models..."
    
    # Install Llama 3.2
    print_status "Installing Llama 3.2..."
    if ollama pull llama3.2; then
        print_status "✅ Llama 3.2 installed successfully"
    else
        print_error "Failed to install Llama 3.2"
        exit 1
    fi
    
    # Install DeepSeek-R1
    print_status "Installing DeepSeek-R1..."
    if ollama pull deepseek-r1:1.5b; then
        print_status "✅ DeepSeek-R1 installed successfully"
    else
        print_error "Failed to install DeepSeek-R1"
        exit 1
    fi
}

# Verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    echo "Installed models:"
    ollama list
    
    echo ""
    print_status "Testing Llama 3.2..."
    echo "Response from Llama 3.2:"
    ollama run llama3.2 "Hello, can you tell me your name and version?" --verbose=false
    
    echo ""
    print_status "Testing DeepSeek-R1..."
    echo "Response from DeepSeek-R1:"
    ollama run deepseek-r1 "Hello, can you tell me your name and version?" --verbose=false
}

# Main installation process
main() {
    echo "This script will:"
    echo "1. Install Ollama"
    echo "2. Start the Ollama service"
    echo "3. Download and install Llama 3.2 model"
    echo "4. Download and install DeepSeek-R1 model"
    echo ""
    echo -n "Do you want to continue? (y/N): "
    read -r response
    
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    
    check_os
    
    if check_ollama; then
        install_ollama
    fi
    
    start_ollama
    install_models
    verify_installation
    
    echo ""
    echo "================================================"
    print_status "🎉 Installation completed successfully!"
    echo ""
    echo "You can now use the models with:"
    echo "  ollama run llama3.2"
    echo "  ollama run deepseek-r1"
    echo ""
    echo "To see all available models: ollama list"
    echo "To stop Ollama service: ollama stop"
    echo "================================================"
}

# Run main function
main "$@"