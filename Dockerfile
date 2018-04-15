# Dockerfile

# Image
FROM python:3-onbuild

# Copy startup script into container
COPY startup.sh /startup.sh

# Expose port 8000 for communication
EXPOSE 8000

# Execute startup command
CMD ["/startup.sh"]

