setupATLAS --quiet
localSetupDQ2Client --quiet
voms-proxy-init -voms atlas
localSetupPandaClient currentJedi --noAthenaCheck

