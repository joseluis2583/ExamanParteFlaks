package com.example;

import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.apache.synapse.MessageContext;
import org.apache.synapse.commons.json.JsonUtil;
import org.apache.synapse.core.axis2.Axis2MessageContext;
import org.apache.synapse.mediators.AbstractMediator;
import org.json.JSONObject;
    
public class SampleMediator extends AbstractMediator { 

    public boolean mediate(MessageContext context) { 
        try {
            org.apache.axis2.context.MessageContext axis2MessageContext = ((Axis2MessageContext) context).getAxis2MessageContext();
            log.info(axis2MessageContext);
            JSONObject jsonPayload = new JSONObject(JsonUtil.jsonPayloadToString(axis2MessageContext));
            log.info(jsonPayload);

           CloseableHttpClient httpClient = HttpClients.createDefault();
            HttpPost httpPost = new HttpPost("http://127.0.0.1:5000/api/bisiesto");
            httpPost.setHeader("Content-Type", "application/json");

            // Configurar el cuerpo de la solicitud
            StringEntity stringEntity = new StringEntity(jsonPayload.toString());
            httpPost.setEntity(stringEntity);
            log.info(httpPost.toString());

            // Ejecutar la solicitud
            try (CloseableHttpResponse response = httpClient.execute(httpPost)) {
                // Obtener la respuesta
                HttpEntity responseEntity = response.getEntity();
                String responseString = EntityUtils.toString(responseEntity);
                log.info("Respuesta del endpoint: " + responseString);
                JsonUtil.newJsonPayload(axis2MessageContext,responseString,true,true);

            }

            } catch(Exception e){
                log.error("Error al procesar el cuerpo del mensaje: ", e);
            }
            return true;
    }
}
