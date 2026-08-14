#!/bin/bash
# Louisiana QSO Party - Quick Start Script
#
# Sets up and starts the Docker containers

set -e

echo "================================================"
echo "Louisiana QSO Party - Docker Quick Start"
echo "================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    echo "Install from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed"
    echo "Install from: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ Created .env file"
        echo ""
        echo "⚠ IMPORTANT: Edit .env and change SECRET_KEY before deploying to production!"
        echo ""
        read -p "Press Enter to continue..."
    else
        echo "Error: .env.example not found"
        exit 1
    fi
fi

# Check if data directory exists
if [ ! -d data ]; then
    echo "⚠ Warning: data/ directory not found"
    echo "Creating data/ directory..."
    mkdir -p data
    echo ""
    echo "You need to add these files to data/:"
    echo "  - LA_County_Abbrevs.txt (all 64 Louisiana counties)"
    echo "  - WVE_Abbrevs.txt (US states and Canadian provinces)"
    echo ""
    read -p "Press Enter to continue (you can add files later)..."
fi

# Check if data files exist
missing_files=()
if [ ! -f data/LA_County_Abbrevs.txt ]; then
    missing_files+=("data/LA_County_Abbrevs.txt")
fi
if [ ! -f data/WVE_Abbrevs.txt ]; then
    missing_files+=("data/WVE_Abbrevs.txt")
fi

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "⚠ Warning: Missing required data files:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "The application may not work correctly without these files."
    read -p "Continue anyway? (y/n): " -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build and start containers
echo ""
echo "Building and starting containers..."
echo ""
docker-compose up -d --build

# Wait for container to be healthy
echo ""
echo "Waiting for application to be ready..."
sleep 5

# Check status
echo ""
echo "Container status:"
docker-compose ps

# Check health
echo ""
echo "Checking application health..."
sleep 2
if curl -f http://localhost:5000/health &> /dev/null; then
    echo "✓ Application is healthy!"
else
    echo "⚠ Application may not be ready yet"
    echo "Check logs with: docker-compose logs -f"
fi

echo ""
echo "================================================"
echo "Louisiana QSO Party is now running!"
echo "================================================"
echo ""
echo "Access the application:"
echo "  - Log Upload:     http://localhost:5000/"
echo "  - Results Lookup: http://localhost:5000/results"
echo "  - Health Check:   http://localhost:5000/health"
echo ""
echo "Useful commands:"
echo "  - View logs:      docker-compose logs -f"
echo "  - Stop:           docker-compose down"
echo "  - Restart:        docker-compose restart"
echo "  - Backup data:    ./backup.sh"
echo ""
echo "To stop the application:"
echo "  docker-compose down"
echo ""
