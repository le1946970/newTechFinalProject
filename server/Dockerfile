FROM frangauthier/final_project_twa_db2:v1_nodejs_python

# Set up your application code
WORKDIR /app
COPY . .

# Install application dependencies
RUN npm install
RUN pip3 install -r requirements.txt

# Expose the port your app runs on
EXPOSE 8080

# Command to run your application
CMD ["npm", "start"]

